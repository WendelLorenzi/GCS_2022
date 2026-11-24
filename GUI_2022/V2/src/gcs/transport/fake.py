"""Fake CanSat: produces realistic C (1 Hz) and T (4 Hz) packets and obeys commands.

``FakeCanSat`` is pure logic driven by an injectable clock (testable).
``FakeLineSource`` runs it in-process, for UI development without hardware.
``tools/fake_cansat.py`` exposes it over TCP / serial / stdout to test the real serial path.

Flight profile (container FSW state machine from the PDR, driven by altitude):
LAUNCH_WAIT -> ASCENT (>10 m) -> ROCKET_SEPARATION (past apogee) -> PC2_RELEASE (<=400 m)
-> TP_RELEASE (<=300 m, payload starts transmitting) -> LANDED (<2 m).
"""

from __future__ import annotations

import datetime as dt
import logging
import math
import queue
import random
import time
from collections.abc import Callable

from gcs.protocol.telemetry import TEAM_ID, format_mission_time, mission_time_seconds
from gcs.transport.base import LineSource, SourceEvent, SourceState

log = logging.getLogger(__name__)

LAUNCH_DELAY = 5.0  # s of LAUNCH_WAIT after CX ON
ASCENT_TIME = 7.0
APOGEE = 700.0
PC2_ALT = 400.0
TP_ALT = 300.0
TETHER_LENGTH = 10.0
TETHER_TIME = 20.0
SITE_LAT, SITE_LON, SITE_MSL = 37.1966, -80.5786, 610.0


def profile_altitude(t: float) -> float:
    """Nominal container altitude (m AGL) ``t`` seconds after launch."""
    if t <= 0:
        return 0.0
    if t < ASCENT_TIME:
        return APOGEE * (1 - (1 - t / ASCENT_TIME) ** 2)
    t -= ASCENT_TIME
    t1 = (APOGEE - PC2_ALT) / 15.0
    if t < t1:
        return APOGEE - 15.0 * t
    return max(PC2_ALT - 5.0 * (t - t1), 0.0)


def pressure_to_altitude(p: float, p0: float) -> float:
    return 44330.0 * (1.0 - (p / p0) ** (1 / 5.255))


class FakeCanSat:
    def __init__(
        self,
        team_id: int = TEAM_ID,
        time_scale: float = 1.0,
        seed: int | None = None,
        telemetry_on: bool = False,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.team_id = team_id
        self.time_scale = time_scale
        self._clock = clock
        self._rng = random.Random(seed)
        self._t0 = clock()
        now_utc = dt.datetime.now(dt.timezone.utc)
        self._utc_base = now_utc.hour * 3600 + now_utc.minute * 60 + now_utc.second

        self.telemetry_on = False
        self._flight_start: float | None = None
        self.packet_count = 0
        self.state = "LAUNCH_WAIT"
        self.tp_state = "STANDBY"
        self.max_alt = 0.0
        self.release_time: float | None = None
        self.sim_enabled = False
        self.sim_active = False
        self._sim_p0: float | None = None
        self._sim_p: float | None = None
        self.cmd_echo = ""
        self._next_c = 0.0
        self._next_t = 0.0
        self._pointing = 90.0
        if telemetry_on:
            self._set_telemetry(True)

    # -- commands --------------------------------------------------------------------------
    def handle_command(self, line: str) -> bool:
        """Apply ``CMD,<id>,<NAME>,<DATA>``. Returns False if ignored."""
        parts = [p.strip() for p in line.strip().split(",")]
        if len(parts) != 4 or parts[0] != "CMD" or parts[1] != str(self.team_id):
            log.warning("fake: ignored %r", line)
            return False
        name, data = parts[2].upper(), parts[3].upper()
        if name == "CX" and data in ("ON", "OFF"):
            self._set_telemetry(data == "ON")
        elif name == "ST":
            if data == "GPS":
                n = dt.datetime.now(dt.timezone.utc)
                secs: float | None = n.hour * 3600 + n.minute * 60 + n.second
            else:
                secs = mission_time_seconds(data)
            if secs is None:
                return False
            self._utc_base = secs - (self._clock() - self._t0)
        elif name == "SIM" and data in ("ENABLE", "ACTIVATE", "DISABLE"):
            if data == "ENABLE":
                self.sim_enabled = True
            elif data == "ACTIVATE":
                if not self.sim_enabled:
                    return False
                self.sim_active = True
            else:
                self.sim_enabled = self.sim_active = False
                self._sim_p0 = self._sim_p = None
        elif name == "SIMP":
            if not self.sim_active:
                return False
            try:
                p = float(data)
            except ValueError:
                return False
            self._sim_p = p
            if self._sim_p0 is None:
                self._sim_p0 = p
        else:
            return False
        self.cmd_echo = name + data
        return True

    def _set_telemetry(self, on: bool) -> None:
        now = self._clock()
        if on and not self.telemetry_on:
            self._next_c = self._next_t = now
            if self._flight_start is None:
                self._flight_start = now + LAUNCH_DELAY / self.time_scale
        self.telemetry_on = on

    # -- simulation ------------------------------------------------------------------------
    def tick(self) -> list[str]:
        """Return all packet lines due since the previous call."""
        now = self._clock()
        if not self.telemetry_on:
            return []
        out: list[tuple[float, str]] = []
        while self._next_c <= now:
            out.append((self._next_c, self._container_line(self._next_c)))
            self._next_c += 1.0
        if self.release_time is None:
            self._next_t = max(self._next_t, now)
        while self.release_time is not None and self._next_t <= now:
            out.append((self._next_t, self._payload_line(self._next_t)))
            self._next_t += 0.25
        out.sort(key=lambda item: item[0])
        return [line for _, line in out]

    def _mission_time(self, t: float) -> str:
        return format_mission_time(self._utc_base + (t - self._t0))

    def _altitude(self, t: float) -> float:
        if self.sim_active:
            if self._sim_p is None or self._sim_p0 is None:
                return 0.0
            return pressure_to_altitude(self._sim_p, self._sim_p0)
        assert self._flight_start is not None
        return profile_altitude((t - self._flight_start) * self.time_scale)

    def _update_state(self, alt: float, t: float) -> None:
        self.max_alt = max(self.max_alt, alt)
        s = self.state
        if s == "LAUNCH_WAIT" and alt > 10:
            self.state = "ASCENT"
        elif s == "ASCENT" and alt < self.max_alt - 10:
            self.state = "ROCKET_SEPARATION"
        elif s == "ROCKET_SEPARATION" and alt <= PC2_ALT:
            self.state = "PC2_RELEASE"
        elif s == "PC2_RELEASE" and alt <= TP_ALT:
            self.state = "TP_RELEASE"
            self.release_time = t
            self._next_t = t
            self.tp_state = "RELEASED"
        elif s == "TP_RELEASE" and alt < 2:
            self.state = "LANDED"
            self.tp_state = "LANDED"

    def _next_count(self) -> int:
        self.packet_count += 1
        return self.packet_count

    def _container_line(self, t: float) -> str:
        alt = self._altitude(t)
        self._update_state(alt, t)
        g = self._rng.gauss
        elapsed = t - self._t0
        fields = [
            str(self.team_id),
            self._mission_time(t),
            str(self._next_count()),
            "C",
            "S" if self.sim_active else "F",
            "N" if self.release_time is None else "R",
            f"{alt + g(0, 0.3):.1f}",
            f"{25.0 - 0.0065 * alt + g(0, 0.1):.1f}",
            f"{7.6 - 0.0005 * elapsed + g(0, 0.01):.2f}",
            format_mission_time(self._utc_base + elapsed)[:8],
            f"{SITE_LAT + g(0, 0.00005):.4f}",
            f"{SITE_LON + g(0, 0.00005):.4f}",
            f"{SITE_MSL + alt + g(0, 1.5):.1f}",
            str(self._rng.randint(7, 11)),
            self.state,
            self.cmd_echo,
        ]
        return ",".join(fields)

    def _payload_line(self, t: float) -> str:
        assert self.release_time is not None
        since = (t - self.release_time) * self.time_scale
        drop = min(TETHER_LENGTH, TETHER_LENGTH * since / TETHER_TIME)
        alt = max(self._altitude(t) - drop, 0.0)
        if self.tp_state != "LANDED":
            self.tp_state = (
                "RELEASED" if since < 5 else "ACQUIRING_TARGET" if since < 10 else "TARGET_POINTING"
            )
        if since >= 5:
            self._pointing *= 0.9
        g = self._rng.gauss
        yaw = math.radians(self._pointing)
        fields = [
            str(self.team_id),
            self._mission_time(t),
            str(self._next_count()),
            "T",
            f"{alt + g(0, 0.3):.1f}",
            f"{25.0 - 0.0065 * alt + g(0, 0.1):.1f}",
            f"{7.5 - 0.0005 * (t - self._t0) + g(0, 0.01):.2f}",
            f"{g(0, 3):.2f}",
            f"{g(0, 3):.2f}",
            f"{-self._pointing * 0.5 + g(0, 2):.2f}",
            f"{g(0, 0.1):.2f}",
            f"{g(0, 0.1):.2f}",
            f"{9.81 + g(0, 0.1):.2f}",
            f"{-0.2 * math.cos(yaw) + g(0, 0.005):.3f}",
            f"{0.2 * math.sin(yaw) + g(0, 0.005):.3f}",
            f"{-0.45 + g(0, 0.005):.3f}",
            f"{self._pointing + g(0, 1.0):.1f}",
            self.tp_state,
        ]
        return ",".join(fields)


class FakeLineSource(LineSource):
    """In-process fake CanSat. Commands sent here go straight to the simulator."""

    can_send = True

    def __init__(
        self,
        events: queue.Queue[SourceEvent],
        time_scale: float = 1.0,
        seed: int | None = None,
        telemetry_on: bool = False,
        period: float = 0.05,
    ) -> None:
        super().__init__(events, name="fake")
        self.cansat = FakeCanSat(time_scale=time_scale, seed=seed, telemetry_on=telemetry_on)
        self.period = period

    def send(self, line: str) -> None:
        if not self.cansat.handle_command(line):
            log.warning("[fake] command rejected: %s", line.strip())

    def _run(self) -> None:
        self._emit_status(SourceState.CONNECTED, "in-process fake CanSat")
        while not self._stop.wait(self.period):
            for text in self.cansat.tick():
                self._emit_line(text)
