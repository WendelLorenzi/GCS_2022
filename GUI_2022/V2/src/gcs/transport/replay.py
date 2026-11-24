"""Replays recorded telemetry (Flight_1038_C.csv / Flight_1038_T.csv or a raw line log).

Lines from all files are merged by PACKET_COUNT (cumulative over C and T packets) and
emitted respecting the MISSION_TIME gaps, divided by ``speed``.
"""

from __future__ import annotations

import logging
import queue
from collections.abc import Sequence
from pathlib import Path

from gcs.protocol.telemetry import TEAM_ID, ParseError, mission_time_seconds, parse_line
from gcs.transport.base import LineSource, SourceEvent, SourceState

log = logging.getLogger(__name__)


def load_lines(paths: Sequence[Path], team_id: int = TEAM_ID) -> list[tuple[float | None, str]]:
    """Read files, drop headers/comments, merge by PACKET_COUNT. Returns (time_s, line)."""
    entries: list[tuple[float, int, float | None, str]] = []  # (order_key, seq, time, line)
    seq = 0
    for path in paths:
        last_key = float("-inf")
        with open(path, encoding="utf-8-sig", newline="") as fh:
            for raw in fh:
                line = raw.strip()
                if not line or line.startswith(("#", "TEAM_ID")):
                    continue
                t: float | None = None
                try:
                    packet = parse_line(line, team_id)
                    last_key = packet.packet_count
                    t = mission_time_seconds(packet.mission_time)
                except ParseError:
                    pass  # keep it next to its neighbour; the consumer will report it
                entries.append((last_key, seq, t, line))
                seq += 1
    entries.sort(key=lambda e: (e[0], e[1]))
    return [(t, line) for _, _, t, line in entries]


class ReplayLineSource(LineSource):
    def __init__(
        self,
        events: queue.Queue[SourceEvent],
        paths: Sequence[str | Path],
        speed: float = 1.0,
        max_gap: float = 5.0,
        loop: bool = False,
        team_id: int = TEAM_ID,
    ) -> None:
        """``speed`` <= 0 emits everything as fast as possible."""
        self.paths = [Path(p) for p in paths]
        super().__init__(events, name="replay:" + ",".join(p.name for p in self.paths))
        self.speed = speed
        self.max_gap = max_gap
        self.loop = loop
        self.team_id = team_id

    def _run(self) -> None:
        lines = load_lines(self.paths, self.team_id)
        self._emit_status(SourceState.CONNECTED, f"{len(lines)} lines")
        while True:
            prev_t: float | None = None
            for t, line in lines:
                if self.speed > 0 and t is not None and prev_t is not None:
                    delay = min(max(t - prev_t, 0.0), self.max_gap) / self.speed
                    if self._stop.wait(delay):
                        return
                elif self._stop.is_set():
                    return
                if t is not None:
                    prev_t = t
                self._emit_line(line)
            if not self.loop:
                break
        self._emit_status(SourceState.FINISHED, f"{len(lines)} lines replayed")
