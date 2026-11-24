"""Builders for GCS -> CanSat commands: ``CMD,<TEAM_ID>,<NAME>,<DATA>``.

Every builder returns the full line including the trailing newline, ready to write to serial.
"""

from __future__ import annotations

import re

from gcs.protocol.telemetry import TEAM_ID

_TIME_RE = re.compile(r"^([01]\d|2[0-3]):[0-5]\d:[0-5]\d$")
_SIM_MODES = ("ENABLE", "ACTIVATE", "DISABLE")


def _cmd(name: str, data: str, team_id: int) -> str:
    return f"CMD,{team_id},{name},{data}\n"


def cx(on: bool, team_id: int = TEAM_ID) -> str:
    """Container telemetry on/off."""
    return _cmd("CX", "ON" if on else "OFF", team_id)


def st(time_utc: str, team_id: int = TEAM_ID) -> str:
    """Set mission time. ``time_utc`` is ``hh:mm:ss`` or ``GPS``."""
    if time_utc != "GPS" and not _TIME_RE.match(time_utc):
        raise ValueError(f"invalid time {time_utc!r}, expected hh:mm:ss or GPS")
    return _cmd("ST", time_utc, team_id)


def sim(mode: str, team_id: int = TEAM_ID) -> str:
    """Simulation mode control: ENABLE, ACTIVATE or DISABLE."""
    mode = mode.upper()
    if mode not in _SIM_MODES:
        raise ValueError(f"invalid SIM mode {mode!r}, expected one of {_SIM_MODES}")
    return _cmd("SIM", mode, team_id)


def simp(pressure_pa: int, team_id: int = TEAM_ID) -> str:
    """Simulated barometric pressure in pascals."""
    if not 0 < pressure_pa < 200_000:
        raise ValueError(f"pressure out of range: {pressure_pa} Pa")
    return _cmd("SIMP", str(int(pressure_pa)), team_id)
