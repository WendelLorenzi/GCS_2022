"""Parsing of CanSat 2022 telemetry lines (container 'C' and tethered payload 'T').

This module is the single source of truth for field order and types. It does no I/O.
"""

from __future__ import annotations

from dataclasses import dataclass, fields

TEAM_ID = 1038

CONTAINER_HEADER: tuple[str, ...] = (
    "TEAM_ID", "MISSION_TIME", "PACKET_COUNT", "PACKET_TYPE", "MODE", "TP_RELEASED",
    "ALTITUDE", "TEMP", "VOLTAGE", "GPS_TIME", "GPS_LATITUDE", "GPS_LONGITUDE",
    "GPS_ALTITUDE", "GPS_SATS", "SOFTWARE_STATE", "CMD_ECHO",
)

PAYLOAD_HEADER: tuple[str, ...] = (
    "TEAM_ID", "MISSION_TIME", "PACKET_COUNT", "PACKET_TYPE", "TP_ALTITUDE", "TP_TEMP",
    "TP_VOLTAGE", "GYRO_R", "GYRO_P", "GYRO_Y", "ACCEL_R", "ACCEL_P", "ACCEL_Y",
    "MAG_R", "MAG_P", "MAG_Y", "POINTING_ERROR", "TP_SOFTWARE_STATE",
)


class ParseError(ValueError):
    """Raised when a line is not a valid C or T telemetry packet."""


@dataclass(frozen=True, slots=True)
class ContainerPacket:
    team_id: int
    mission_time: str
    packet_count: int
    packet_type: str
    mode: str
    tp_released: str
    altitude: float | None
    temp: float | None
    voltage: float | None
    gps_time: str
    gps_latitude: float | None
    gps_longitude: float | None
    gps_altitude: float | None
    gps_sats: int | None
    software_state: str
    cmd_echo: str
    raw: tuple[str, ...]  # fields exactly as received, for CSV output


@dataclass(frozen=True, slots=True)
class PayloadPacket:
    team_id: int
    mission_time: str
    packet_count: int
    packet_type: str
    tp_altitude: float | None
    tp_temp: float | None
    tp_voltage: float | None
    gyro_r: float | None
    gyro_p: float | None
    gyro_y: float | None
    accel_r: float | None
    accel_p: float | None
    accel_y: float | None
    mag_r: float | None
    mag_p: float | None
    mag_y: float | None
    pointing_error: float | None
    tp_software_state: str
    raw: tuple[str, ...]


Packet = ContainerPacket | PayloadPacket


def _opt_float(value: str, name: str) -> float | None:
    if value == "":
        return None
    try:
        return float(value)
    except ValueError as exc:
        raise ParseError(f"{name}: expected number, got {value!r}") from exc


def _opt_int(value: str, name: str) -> int | None:
    if value == "":
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise ParseError(f"{name}: expected integer, got {value!r}") from exc


def _req_int(value: str, name: str) -> int:
    result = _opt_int(value, name)
    if result is None:
        raise ParseError(f"{name}: required field is empty")
    return result


def _convert(cls: type, header: tuple[str, ...], parts: tuple[str, ...]) -> Packet:
    kwargs: dict[str, object] = {}
    for f, name, value in zip(fields(cls), header, parts):
        if f.name in ("team_id", "packet_count"):
            kwargs[f.name] = _req_int(value, name)
        elif f.type == "int | None":
            kwargs[f.name] = _opt_int(value, name)
        elif f.type == "float | None":
            kwargs[f.name] = _opt_float(value, name)
        else:
            kwargs[f.name] = value
    return cls(**kwargs, raw=parts)


def mission_time_seconds(value: str) -> float | None:
    """``hh:mm:ss`` or ``hh:mm:ss.ss`` -> seconds since midnight; None if malformed."""
    try:
        hh, mm, ss = value.split(":")
        h, m, s = int(hh), int(mm), float(ss)
    except ValueError:
        return None
    if not (0 <= h < 24 and 0 <= m < 60 and 0 <= s < 60):
        return None
    return h * 3600 + m * 60 + s


def format_mission_time(seconds: float) -> str:
    """Seconds since midnight -> ``hh:mm:ss.ss`` (wraps at 24 h)."""
    centis = round(seconds * 100) % (24 * 3600 * 100)
    h, rem = divmod(centis, 3600 * 100)
    m, rem = divmod(rem, 60 * 100)
    return f"{h:02d}:{m:02d}:{rem / 100:05.2f}"


def parse_line(line: str, expected_team_id: int = TEAM_ID) -> Packet:
    """Parse one telemetry line into a ContainerPacket or PayloadPacket.

    Raises ParseError for anything that is not a well-formed C/T packet of this team.
    """
    text = line.strip()
    if not text:
        raise ParseError("empty line")
    parts = tuple(p.strip() for p in text.split(","))
    if len(parts) < 4:
        raise ParseError(f"too few fields ({len(parts)})")

    packet_type = parts[3].upper()
    if packet_type == "C":
        cls, header = ContainerPacket, CONTAINER_HEADER
    elif packet_type == "T":
        cls, header = PayloadPacket, PAYLOAD_HEADER
    else:
        raise ParseError(f"unknown PACKET_TYPE {parts[3]!r}")

    if len(parts) != len(header):
        raise ParseError(
            f"packet {packet_type}: expected {len(header)} fields, got {len(parts)}"
        )

    packet = _convert(cls, header, parts)
    if packet.team_id != expected_team_id:
        raise ParseError(f"TEAM_ID {packet.team_id} != {expected_team_id}")
    return packet
