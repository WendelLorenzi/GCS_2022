"""Flight CSV files required by the judges: Flight_<TEAM_ID>_C.csv and Flight_<TEAM_ID>_T.csv.

Each session gets its own folder (``<output_dir>/<YYYYmmdd_HHMMSS>/``) so a previous flight is
never overwritten; inside it the files keep the official names. Every packet is appended and
flushed immediately, so a crash loses at most the line being written.
"""

from __future__ import annotations

import datetime as dt
import logging
import shutil
from collections.abc import Callable
from pathlib import Path
from typing import TextIO

from gcs.protocol.telemetry import (
    CONTAINER_HEADER,
    PAYLOAD_HEADER,
    TEAM_ID,
    ContainerPacket,
    Packet,
)

log = logging.getLogger(__name__)


def flight_filenames(team_id: int = TEAM_ID) -> tuple[str, str]:
    return f"Flight_{team_id}_C.csv", f"Flight_{team_id}_T.csv"


class CsvFlightWriter:
    """PacketSink that writes the official flight CSVs."""

    def __init__(
        self,
        output_dir: str | Path,
        team_id: int = TEAM_ID,
        now: Callable[[], dt.datetime] = dt.datetime.now,
    ) -> None:
        self.output_dir = Path(output_dir)
        self.team_id = team_id
        self._now = now
        self.session_dir: Path | None = None  # kept after close, for "save to USB drive"
        self._files: dict[str, TextIO] = {}
        self._warned_closed = False
        self.rows_written = {"C": 0, "T": 0}
        # False = do not record the next sessions (e.g. replay). Change only between sessions.
        self.enabled = True
        self.recording = False

    @property
    def paths(self) -> tuple[Path, Path] | None:
        if self.session_dir is None:
            return None
        c, t = flight_filenames(self.team_id)
        return self.session_dir / c, self.session_dir / t

    # -- PacketSink ------------------------------------------------------------------------
    def open_session(self) -> None:
        self.close_session()
        if not self.enabled:
            log.info("flight recording disabled for this session")
            return
        session_dir = self._new_session_dir()
        c_name, t_name = flight_filenames(self.team_id)
        for kind, name, header in (("C", c_name, CONTAINER_HEADER), ("T", t_name, PAYLOAD_HEADER)):
            fh = open(session_dir / name, "x", encoding="utf-8", newline="")  # noqa: SIM115 - open for the whole session
            fh.write(",".join(header) + "\n")
            fh.flush()
            self._files[kind] = fh
        self.session_dir = session_dir
        self.rows_written = {"C": 0, "T": 0}
        self._warned_closed = False
        self.recording = True
        log.info("recording flight to %s", session_dir)

    def on_packet(self, packet: Packet) -> None:
        kind = "C" if isinstance(packet, ContainerPacket) else "T"
        fh = self._files.get(kind)
        if fh is None:
            if not self.enabled:
                return
            if not self._warned_closed:
                log.error("CSV not open: packets are NOT being recorded")
                self._warned_closed = True
            return
        fh.write(",".join(packet.raw) + "\n")
        fh.flush()
        self.rows_written[kind] += 1

    def close_session(self) -> None:
        if not self._files:
            return
        for fh in self._files.values():
            try:
                fh.close()
            except OSError:
                log.exception("error closing %s", fh.name)
        self._files.clear()
        self.recording = False
        log.info(
            "flight saved in %s (C=%d, T=%d rows)",
            self.session_dir, self.rows_written["C"], self.rows_written["T"],
        )

    # -- helpers ---------------------------------------------------------------------------
    def copy_to(self, dest: str | Path, overwrite: bool = False) -> list[Path]:
        """Copy the last session's CSVs to ``dest`` (e.g. the judges' USB drive)."""
        if self._files:
            raise RuntimeError("stop the session before copying the flight files")
        paths = self.paths
        if paths is None:
            raise RuntimeError("no flight recorded yet")
        dest = Path(dest)
        dest.mkdir(parents=True, exist_ok=True)
        copied = []
        for src in paths:
            target = dest / src.name
            if target.exists() and not overwrite:
                raise FileExistsError(target)
            shutil.copy2(src, target)
            copied.append(target)
        log.info("flight files copied to %s", dest)
        return copied

    def _new_session_dir(self) -> Path:
        stamp = self._now().strftime("%Y%m%d_%H%M%S")
        for i in range(1, 100):
            candidate = self.output_dir / (stamp if i == 1 else f"{stamp}_{i}")
            try:
                candidate.mkdir(parents=True)
                return candidate
            except FileExistsError:
                continue
        raise FileExistsError(f"cannot create a session folder for {stamp} in {self.output_dir}")
