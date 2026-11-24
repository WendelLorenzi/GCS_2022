"""In-memory telemetry for the UI: recent packets per type, last values and link statistics.

Not thread-safe by design: only the main thread (MissionController.poll) writes to it.
"""

from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass, fields
from typing import Literal

from gcs.protocol.telemetry import ContainerPacket, Packet, PayloadPacket, mission_time_seconds

PacketKind = Literal["C", "T"]
_DAY = 24 * 3600.0
_FIELDS = {
    "C": {f.name for f in fields(ContainerPacket)} - {"raw"},
    "T": {f.name for f in fields(PayloadPacket)} - {"raw"},
}


@dataclass
class LinkStats:
    received_c: int = 0
    received_t: int = 0
    invalid: int = 0  # lines that failed to parse
    lost: int = 0  # gaps in the cumulative PACKET_COUNT
    resets: int = 0  # PACKET_COUNT went backwards (CanSat reset / replay loop)

    @property
    def received(self) -> int:
        return self.received_c + self.received_t


class TelemetryStore:
    def __init__(self, maxlen: int = 300) -> None:
        self.maxlen = maxlen
        self.clear()

    def clear(self) -> None:
        self.container: deque[ContainerPacket] = deque(maxlen=self.maxlen)
        self.payload: deque[PayloadPacket] = deque(maxlen=self.maxlen)
        self.stats = LinkStats()
        self.last_container: ContainerPacket | None = None
        self.last_payload: PayloadPacket | None = None
        self.last_packet_count: int | None = None
        self.t0: float | None = None  # mission time (s) of the first packet; plot origin
        self.version = 0  # bumps on every change; UI redraws only when it moves

    def add(self, packet: Packet) -> None:
        self._track_count(packet.packet_count)
        if self.t0 is None:
            self.t0 = mission_time_seconds(packet.mission_time)
        if isinstance(packet, ContainerPacket):
            self.container.append(packet)
            self.last_container = packet
            self.stats.received_c += 1
        else:
            self.payload.append(packet)
            self.last_payload = packet
            self.stats.received_t += 1
        self.version += 1

    def add_invalid(self) -> None:
        self.stats.invalid += 1
        self.version += 1

    def _track_count(self, count: int) -> None:
        last = self.last_packet_count
        if last is not None:
            if count > last + 1:
                self.stats.lost += count - last - 1
            elif count <= last:
                self.stats.resets += 1
        self.last_packet_count = count

    def relative_time(self, mission_time: str) -> float:
        """Seconds since the first packet of the session (handles midnight wrap)."""
        t = mission_time_seconds(mission_time)
        if t is None or self.t0 is None:
            return math.nan
        dt = t - self.t0
        return dt + _DAY if dt < -_DAY / 2 else dt

    def series(self, kind: PacketKind, field: str) -> tuple[list[float], list[float]]:
        """(x = seconds since first packet, y = field values; missing -> NaN) for plotting."""
        if field not in _FIELDS[kind]:
            raise ValueError(f"unknown field {field!r} for packet {kind}")
        packets = self.container if kind == "C" else self.payload
        xs: list[float] = []
        ys: list[float] = []
        for p in packets:
            value = getattr(p, field)
            xs.append(self.relative_time(p.mission_time))
            ys.append(math.nan if value is None else float(value))
        return xs, ys
