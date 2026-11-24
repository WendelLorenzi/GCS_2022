"""Simulation mode: SIM ENABLE -> SIM ACTIVATE -> one SIMP per second from a pressure profile.

Driven by ``tick()`` from the main thread (no extra thread). Commands go out through the
``send`` callable (MissionController.send_command), which returns False on failure.
"""

from __future__ import annotations

import enum
import logging
import time
from collections.abc import Callable, Iterable
from pathlib import Path

from gcs.protocol import commands
from gcs.protocol.telemetry import TEAM_ID, ContainerPacket, Packet

log = logging.getLogger(__name__)

MIN_PA, MAX_PA = 1, 199_999  # same range accepted by commands.simp


class SimState(enum.Enum):
    IDLE = "idle"
    ENABLED = "enabled"
    RUNNING = "running"
    FINISHED = "finished"  # profile exhausted; CanSat still in simulation mode


def parse_simp_profile(lines: Iterable[str]) -> list[int]:
    """Pressures (Pa) from a profile.

    Accepts the competition format ``CMD,$,SIMP,<Pa>`` (``$`` or any team id) and bare
    numbers, one per line. ``#`` comments and blank lines are ignored.
    """
    pressures: list[int] = []
    for n, raw in enumerate(lines, start=1):
        line = raw.strip().lstrip("﻿")
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) == 4 and parts[0].upper() == "CMD" and parts[2].upper() == "SIMP":
            value = parts[3]
        elif len(parts) == 1:
            value = parts[0]
        else:
            raise ValueError(f"line {n}: unexpected format {line!r}")
        try:
            pa = round(float(value))
        except ValueError as exc:
            raise ValueError(f"line {n}: invalid pressure {value!r}") from exc
        if not MIN_PA <= pa <= MAX_PA:
            raise ValueError(f"line {n}: pressure out of range ({pa} Pa)")
        pressures.append(pa)
    if not pressures:
        raise ValueError("profile has no pressures")
    return pressures


def load_simp_profile(path: str | Path) -> list[int]:
    with open(path, encoding="utf-8-sig") as fh:
        return parse_simp_profile(fh)


class SimulationRunner:
    def __init__(
        self,
        send: Callable[[str], bool],
        team_id: int = TEAM_ID,
        period: float = 1.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._send = send
        self.team_id = team_id
        self.period = period
        self._clock = clock
        self.pressures: list[int] = []
        self.profile_name = ""
        self.state = SimState.IDLE
        self.index = 0  # next pressure to send
        self.confirmed = False  # CanSat reported MODE=S
        self._next_send = 0.0

    # -- profile ---------------------------------------------------------------------------
    def load(self, pressures: list[int], name: str = "") -> None:
        if self.state is SimState.RUNNING:
            raise RuntimeError("cannot change profile while running")
        self.pressures = list(pressures)
        self.profile_name = name
        self.index = 0
        log.info("simulation profile loaded: %d pressures %s", len(self.pressures), name)

    def load_file(self, path: str | Path) -> None:
        self.load(load_simp_profile(path), Path(path).name)

    @property
    def progress(self) -> tuple[int, int]:
        return self.index, len(self.pressures)

    # -- operator actions ------------------------------------------------------------------
    def enable(self) -> bool:
        if not self._send(commands.sim("ENABLE", self.team_id)):
            return False
        self.state = SimState.ENABLED
        return True

    def activate(self) -> bool:
        if self.state is not SimState.ENABLED:
            log.warning("SIM ACTIVATE refused: send SIM ENABLE first")
            return False
        if not self.pressures:
            log.warning("SIM ACTIVATE refused: no pressure profile loaded")
            return False
        if not self._send(commands.sim("ACTIVATE", self.team_id)):
            return False
        self.state = SimState.RUNNING
        self.index = 0
        self._next_send = self._clock()
        return True

    def disable(self) -> bool:
        sent = self._send(commands.sim("DISABLE", self.team_id))
        self.halt()
        return sent

    def halt(self) -> None:
        """Stop streaming locally (no command). Used when the session ends."""
        if self.state in (SimState.RUNNING, SimState.ENABLED):
            log.info("simulation halted at %d/%d", self.index, len(self.pressures))
        self.state = SimState.IDLE
        self.confirmed = False

    # -- driven by the controller ----------------------------------------------------------
    def tick(self) -> None:
        if self.state is not SimState.RUNNING:
            return
        now = self._clock()
        if now < self._next_send:
            return
        line = commands.simp(self.pressures[self.index], self.team_id)
        if self._send(line):
            self.index += 1
        # on failure the same pressure is retried next period
        # keep a steady 1 Hz grid; after a stall restart from "now" instead of bursting
        self._next_send += self.period
        if self._next_send <= now:
            self._next_send = now + self.period
        if self.index >= len(self.pressures):
            self.state = SimState.FINISHED
            log.info("simulation profile finished (%d pressures)", self.index)

    def on_packet(self, packet: Packet) -> None:
        if isinstance(packet, ContainerPacket):
            self.confirmed = packet.mode == "S"
