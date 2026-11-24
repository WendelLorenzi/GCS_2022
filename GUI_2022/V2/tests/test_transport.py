import queue
import time

import pytest
import serial

from gcs.protocol import commands
from gcs.protocol.telemetry import (
    CONTAINER_HEADER,
    PAYLOAD_HEADER,
    ContainerPacket,
    PayloadPacket,
    format_mission_time,
    mission_time_seconds,
    parse_line,
)
from gcs.transport import (
    CommandNotSupported,
    FakeCanSat,
    FakeLineSource,
    LineAssembler,
    LineReceived,
    ReplayLineSource,
    SerialLineSource,
    SourceState,
    SourceStatus,
)


def collect(events, until, timeout=3.0):
    """Drain events until ``until(collected)`` is true or timeout."""
    got = []
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline and not until(got):
        try:
            got.append(events.get(timeout=0.05))
        except queue.Empty:
            pass
    return got


def lines(evts):
    return [e.text for e in evts if isinstance(e, LineReceived)]


def states(evts):
    return [e.state for e in evts if isinstance(e, SourceStatus)]


# -- mission time -------------------------------------------------------------------------
def test_mission_time_roundtrip():
    assert mission_time_seconds("13:35:59.25") == pytest.approx(48959.25)
    assert mission_time_seconds("13:35:59") == 48959
    assert mission_time_seconds("bad") is None
    assert mission_time_seconds("25:00:00") is None
    assert format_mission_time(48959.25) == "13:35:59.25"
    assert format_mission_time(86400.5) == "00:00:00.50"


# -- framing ------------------------------------------------------------------------------
def test_line_assembler_split_and_crlf():
    a = LineAssembler()
    assert a.feed(b"1038,1") == []
    assert a.feed(b"2\r\n\r\nabc\nde") == ["1038,12", "abc"]
    assert a.feed(b"f\n") == ["def"]


def test_line_assembler_discards_garbage():
    a = LineAssembler(max_line=10)
    assert a.feed(b"x" * 20) == []
    assert a.discarded_bytes == 20
    assert a.feed(b"ok\n") == ["ok"]


# -- serial -------------------------------------------------------------------------------
def test_serial_loopback_send_and_receive():
    events = queue.Queue()
    src = SerialLineSource(events, "loop://", reconnect_interval=0.05)
    src.start()
    try:
        collect(events, lambda g: SourceState.CONNECTED in states(g))
        src.send(commands.cx(True))
        got = collect(events, lambda g: len(lines(g)) >= 1)
        assert lines(got) == ["CMD,1038,CX,ON"]
    finally:
        src.stop()
    assert not src.running


def test_serial_reconnects_after_open_failure():
    attempts = {"n": 0}

    def flaky_factory(port, **kw):
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise serial.SerialException("port busy")
        return serial.serial_for_url("loop://", **kw)

    events = queue.Queue()
    src = SerialLineSource(events, "COM99", reconnect_interval=0.01, serial_factory=flaky_factory)
    src.start()
    try:
        got = collect(events, lambda g: SourceState.CONNECTED in states(g))
    finally:
        src.stop()
    assert states(got)[:3] == [SourceState.DISCONNECTED, SourceState.DISCONNECTED, SourceState.CONNECTED]


def test_serial_send_when_disconnected_raises():
    src = SerialLineSource(queue.Queue(), "loop://")
    with pytest.raises(ConnectionError):
        src.send("CMD,1038,CX,ON\n")


# -- replay -------------------------------------------------------------------------------
def test_replay_merges_by_packet_count(tmp_path):
    c = tmp_path / "Flight_1038_C.csv"
    t = tmp_path / "Flight_1038_T.csv"
    c_rows = [
        "1038,10:00:00.00,1,C,F,N,0.0,25.0,7.50,10:00:00,37.1966,-80.5786,610.0,8,LAUNCH_WAIT,CXON",
        "1038,10:00:01.00,4,C,F,R,300.0,23.0,7.50,10:00:01,37.1966,-80.5786,910.0,8,TP_RELEASE,CXON",
    ]
    t_rows = [
        "1038,10:00:00.25,2,T,300.0,23,7.4,0,0,0,0,0,9.8,0.1,0.1,-0.4,90,RELEASED",
        "1038,10:00:00.50,3,T,299.5,23,7.4,0,0,0,0,0,9.8,0.1,0.1,-0.4,80,RELEASED",
    ]
    c.write_text("﻿" + ",".join(CONTAINER_HEADER) + "\n" + "\n".join(c_rows) + "\n", "utf-8")
    t.write_text(",".join(PAYLOAD_HEADER) + "\n" + "\n".join(t_rows) + "\n", "utf-8")

    events = queue.Queue()
    src = ReplayLineSource(events, [c, t], speed=0)
    src.start()
    got = collect(events, lambda g: SourceState.STOPPED in states(g))
    counts = [parse_line(x).packet_count for x in lines(got)]
    assert counts == [1, 2, 3, 4]
    assert SourceState.FINISHED in states(got)
    with pytest.raises(CommandNotSupported):
        src.send("CMD,1038,CX,ON\n")


def test_replay_respects_timing(tmp_path):
    f = tmp_path / "log.txt"
    f.write_text(
        "1038,10:00:00.00,1,C,F,N,0,25,7.5,10:00:00,0,0,0,0,LAUNCH_WAIT,\n"
        "1038,10:00:01.00,2,C,F,N,0,25,7.5,10:00:01,0,0,0,0,LAUNCH_WAIT,\n"
    )
    events = queue.Queue()
    src = ReplayLineSource(events, [f], speed=4)  # 1 s gap -> 0.25 s
    t0 = time.monotonic()
    src.start()
    collect(events, lambda g: SourceState.STOPPED in states(g))
    assert 0.2 <= time.monotonic() - t0 < 1.0


# -- fake CanSat --------------------------------------------------------------------------
class FakeClock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t


def run_fake(cansat, clock, seconds, step=0.05):
    out = []
    for _ in range(round(seconds / step)):
        clock.t += step
        out += cansat.tick()
    return [parse_line(x) for x in out]


def test_fake_silent_until_cx_on():
    clock = FakeClock()
    cs = FakeCanSat(seed=1, clock=clock)
    assert run_fake(cs, clock, 3) == []
    assert cs.handle_command(commands.cx(True))
    pkts = run_fake(cs, clock, 3)
    assert len(pkts) == 3 and all(isinstance(p, ContainerPacket) for p in pkts)
    assert pkts[-1].cmd_echo == "CXON"


def test_fake_full_flight_follows_fsw_states():
    clock = FakeClock()
    cs = FakeCanSat(seed=1, clock=clock, telemetry_on=True, time_scale=4)
    pkts = run_fake(cs, clock, 40)
    c = [p for p in pkts if isinstance(p, ContainerPacket)]
    t = [p for p in pkts if isinstance(p, PayloadPacket)]

    seen = list(dict.fromkeys(p.software_state for p in c))
    assert seen == ["LAUNCH_WAIT", "ASCENT", "ROCKET_SEPARATION", "PC2_RELEASE", "TP_RELEASE", "LANDED"]
    assert [p.packet_count for p in pkts] == list(range(1, len(pkts) + 1))
    assert t, "payload must transmit after release"
    assert 3.5 <= len(t) / (len(c) - c.index(next(p for p in c if p.tp_released == "R"))) <= 4.5
    assert t[0].tp_altitude <= c[-1].altitude + 400  # sanity
    assert t[-1].pointing_error < 10


def test_fake_simulation_mode():
    clock = FakeClock()
    cs = FakeCanSat(seed=1, clock=clock, telemetry_on=True)
    assert not cs.handle_command(commands.sim("ACTIVATE"))  # needs ENABLE first
    assert not cs.handle_command(commands.simp(101325))  # ignored while inactive
    assert cs.handle_command(commands.sim("ENABLE"))
    assert cs.handle_command(commands.sim("ACTIVATE"))
    assert cs.handle_command(commands.simp(101325))  # ground reference
    assert cs.handle_command(commands.simp(95000))  # ~ 540 m
    p = run_fake(cs, clock, 1.05)[-1]
    assert p.mode == "S"
    assert 520 < p.altitude < 560
    assert p.cmd_echo == "SIMP95000"
    assert cs.handle_command(commands.sim("DISABLE"))
    assert run_fake(cs, clock, 1.05)[-1].mode == "F"


def test_fake_set_time():
    clock = FakeClock()
    cs = FakeCanSat(clock=clock, telemetry_on=True)
    assert cs.handle_command(commands.st("13:00:00"))
    assert run_fake(cs, clock, 1.0)[0].mission_time.startswith("13:00:0")
    assert not cs.handle_command("CMD,9999,CX,ON")


def test_fake_line_source_end_to_end():
    events = queue.Queue()
    src = FakeLineSource(events, seed=1, period=0.01)
    src.start()
    try:
        collect(events, lambda g: SourceState.CONNECTED in states(g))
        src.send(commands.cx(True))
        got = collect(events, lambda g: len(lines(g)) >= 2, timeout=3)
    finally:
        src.stop()
    assert [parse_line(x).packet_type for x in lines(got)] == ["C", "C"]
