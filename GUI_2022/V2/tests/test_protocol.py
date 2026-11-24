import pytest

from gcs.protocol import commands
from gcs.protocol.telemetry import (
    CONTAINER_HEADER,
    PAYLOAD_HEADER,
    ContainerPacket,
    ParseError,
    PayloadPacket,
    parse_line,
)

C_LINE = (
    "1038,13:35:59.25,42,C,F,N,512.3,24.1,7.42,13:35:59,"
    "-25.4284,-49.2733,1430.2,8,ROCKET_SEPARATION,CXON"
)
T_LINE = (
    "1038,13:36:10.50,57,T,280.4,22.8,7.31,1.2,-3.4,0.5,"
    "0.01,-0.02,9.81,0.21,-0.03,0.44,4.5,TARGET_POINTING"
)


def test_parse_container():
    p = parse_line(C_LINE + "\r\n")
    assert isinstance(p, ContainerPacket)
    assert p.packet_count == 42
    assert p.altitude == 512.3
    assert p.gps_sats == 8
    assert p.software_state == "ROCKET_SEPARATION"
    assert len(p.raw) == len(CONTAINER_HEADER)


def test_parse_payload():
    p = parse_line(T_LINE)
    assert isinstance(p, PayloadPacket)
    assert p.mag_p == -0.03
    assert p.accel_y == 9.81
    assert p.pointing_error == 4.5
    assert len(p.raw) == len(PAYLOAD_HEADER)


def test_empty_optional_fields_become_none():
    line = C_LINE.replace("-25.4284,-49.2733,1430.2,8", ",,,")
    p = parse_line(line)
    assert p.gps_latitude is None and p.gps_sats is None


@pytest.mark.parametrize(
    "line",
    [
        "",
        "1038,13:00:00,1",
        C_LINE.replace(",C,", ",Z,"),
        C_LINE + ",extra",
        C_LINE.replace("512.3", "abc"),
        C_LINE.replace("1038,", "9999,", 1),
    ],
)
def test_invalid_lines(line):
    with pytest.raises(ParseError):
        parse_line(line)


def test_headers_match_official_csv():
    assert CONTAINER_HEADER[-1] == "CMD_ECHO" and len(CONTAINER_HEADER) == 16
    assert PAYLOAD_HEADER[-1] == "TP_SOFTWARE_STATE" and len(PAYLOAD_HEADER) == 18


def test_commands():
    assert commands.cx(True) == "CMD,1038,CX,ON\n"
    assert commands.cx(False) == "CMD,1038,CX,OFF\n"
    assert commands.st("13:35:59") == "CMD,1038,ST,13:35:59\n"
    assert commands.st("GPS") == "CMD,1038,ST,GPS\n"
    assert commands.sim("enable") == "CMD,1038,SIM,ENABLE\n"
    assert commands.simp(101325) == "CMD,1038,SIMP,101325\n"


@pytest.mark.parametrize(
    "call",
    [
        lambda: commands.st("25:00:00"),
        lambda: commands.sim("START"),
        lambda: commands.simp(0),
    ],
)
def test_invalid_commands(call):
    with pytest.raises(ValueError):
        call()
