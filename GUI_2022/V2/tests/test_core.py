import math
import time

import pytest

from gcs.core import (
    MissionController,
    SimState,
    SimulationRunner,
    TelemetryStore,
    parse_simp_profile,
)
from gcs.protocol.telemetry import parse_line
from gcs.transport import FakeLineSource, LineSource, SourceState


def c_line(count, t="10:00:00.00", alt="100.0", mode="F", gps_lat="37.1966"):
    return (
        f"1038,{t},{count},C,{mode},N,{alt},25.0,7.50,10:00:00,{gps_lat},-80.5786,710.0,8,"
        "ASCENT,CXON"
    )


def t_line(count, t="10:00:00.25"):
    return f"1038,{t},{count},T,90.0,24.0,7.40,1,2,3,0,0,9.8,0.1,0.2,-0.4,12.5,TARGET_POINTING"


class FakeClock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


class ScriptedSource(LineSource):
    """Emits the given lines once, then idles until stopped. Records commands."""

    can_send = True

    def __init__(self, events, lines):
        super().__init__(events, name="scripted")
        self.lines = lines
        self.sent = []

    def send(self, line):
        self.sent.append(line)

    def _run(self):
        self._emit_status(SourceState.CONNECTED)
        for text in self.lines:
            self._emit_line(text)
        self._stop.wait()


class RecordingSink:
    def __init__(self):
        self.calls = []

    def open_session(self):
        self.calls.append("open")

    def on_packet(self, packet):
        self.calls.append(packet.packet_count)

    def close_session(self):
        self.calls.append("close")


def pump(ctrl, until, timeout=3.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline and not until():
        ctrl.poll()
        time.sleep(0.01)
    return until()


# -- store --------------------------------------------------------------------------------
def test_store_stats_and_last_values():
    s = TelemetryStore()
    for line in (c_line(1), t_line(2), t_line(5), c_line(6)):
        s.add(parse_line(line))
    s.add_invalid()
    assert (s.stats.received_c, s.stats.received_t, s.stats.received) == (2, 2, 4)
    assert s.stats.lost == 2  # counts 3 and 4 missing
    assert s.stats.invalid == 1
    assert s.last_container.packet_count == 6 and s.last_payload.packet_count == 5
    s.add(parse_line(c_line(1)))
    assert s.stats.resets == 1


def test_store_series_relative_time_and_nan():
    s = TelemetryStore()
    s.add(parse_line(c_line(1, t="23:59:59.00", alt="10.0")))
    s.add(parse_line(c_line(2, t="00:00:01.00", alt="", gps_lat="")))
    xs, ys = s.series("C", "altitude")
    assert xs == [0.0, 2.0]  # midnight wrap handled
    assert ys[0] == 10.0 and math.isnan(ys[1])
    with pytest.raises(ValueError):
        s.series("C", "gyro_r")


def test_store_maxlen_and_version():
    s = TelemetryStore(maxlen=3)
    v = s.version
    for i in range(1, 6):
        s.add(parse_line(c_line(i)))
    assert len(s.container) == 3 and s.container[0].packet_count == 3
    assert s.version == v + 5


# -- simulation profile -------------------------------------------------------------------
def test_parse_simp_profile_formats():
    text = ["﻿# header", "", "CMD,$,SIMP,101325", "CMD,1038,SIMP,101300.4", "101200"]
    assert parse_simp_profile(text) == [101325, 101300, 101200]


@pytest.mark.parametrize("text", [[], ["# only comments"], ["CMD,$,SIMP,abc"], ["1,2"], ["0"]])
def test_parse_simp_profile_errors(text):
    with pytest.raises(ValueError):
        parse_simp_profile(text)


# -- simulation runner --------------------------------------------------------------------
def make_runner(ok=True):
    sent, clock = [], FakeClock()

    def send(line):
        if ok:
            sent.append(line.strip())
        return ok

    return SimulationRunner(send, clock=clock), sent, clock


def test_simulation_requires_enable_and_profile():
    r, sent, _ = make_runner()
    assert not r.activate()
    assert r.enable()
    assert not r.activate()  # no profile yet
    r.load([101325])
    assert r.activate()
    assert sent == ["CMD,1038,SIM,ENABLE", "CMD,1038,SIM,ACTIVATE"]


def test_simulation_streams_at_1hz_without_bursts():
    r, sent, clock = make_runner()
    r.load([101325, 101000, 100500, 100000])
    r.enable()
    r.activate()
    sent.clear()
    for _ in range(25):  # 2.5 s polled at 10 Hz
        r.tick()
        clock.t += 0.1
    assert sent == ["CMD,1038,SIMP,101325", "CMD,1038,SIMP,101000", "CMD,1038,SIMP,100500"]
    clock.t += 30  # UI froze for 30 s
    r.tick()
    r.tick()
    assert sent[-1] == "CMD,1038,SIMP,100000" and len(sent) == 4
    assert r.state is SimState.FINISHED and r.progress == (4, 4)


def test_simulation_retries_on_send_failure_and_disable():
    r, sent, clock = make_runner()
    r.load([101325, 101000])
    r.enable()
    r.activate()
    r._send = lambda line: False  # link dropped
    r.tick()
    assert r.index == 0
    r._send = lambda line: sent.append(line.strip()) or True
    clock.t += 1.0
    r.tick()
    assert r.index == 1 and sent[-1] == "CMD,1038,SIMP,101325"
    assert r.disable() and sent[-1] == "CMD,1038,SIM,DISABLE"
    assert r.state is SimState.IDLE


def test_simulation_confirmation_from_telemetry():
    r, _, _ = make_runner()
    r.on_packet(parse_line(c_line(1, mode="S")))
    assert r.confirmed
    r.on_packet(parse_line(t_line(2)))  # T packets don't change it
    assert r.confirmed
    r.on_packet(parse_line(c_line(3, mode="F")))
    assert not r.confirmed


# -- controller ---------------------------------------------------------------------------
def test_controller_session_routes_packets_and_commands():
    store, sink = TelemetryStore(), RecordingSink()
    ctrl = MissionController(store, sinks=[sink])
    holder = {}

    def factory(events):
        holder["src"] = ScriptedSource(events, [c_line(1), "garbage", t_line(2), c_line(3)])
        return holder["src"]

    ctrl.start_session(factory)
    assert pump(ctrl, lambda: store.stats.received == 3)
    assert ctrl.source_state is SourceState.CONNECTED
    assert store.stats.invalid == 1
    assert ctrl.set_telemetry(True)
    assert holder["src"].sent == ["CMD,1038,CX,ON\n"]
    assert ctrl.last_command == "CMD,1038,CX,ON"
    ctrl.stop_session()
    assert sink.calls == ["open", 1, 2, 3, "close"]
    assert not ctrl.session_active
    assert ctrl.source_state is SourceState.STOPPED
    assert not ctrl.set_telemetry(False)  # no session


def test_controller_stop_drains_queue():
    store = TelemetryStore()
    ctrl = MissionController(store)
    ctrl.start_session(lambda q: ScriptedSource(q, [c_line(i) for i in range(1, 51)]))
    time.sleep(0.2)  # lines queued, never polled
    ctrl.stop_session()
    assert store.stats.received_c == 50


def test_controller_isolates_broken_sink():
    class Broken(RecordingSink):
        def on_packet(self, packet):
            raise RuntimeError("disk full")

    store, good = TelemetryStore(), RecordingSink()
    ctrl = MissionController(store, sinks=[Broken(), good])
    ctrl.start_session(lambda q: ScriptedSource(q, [c_line(1), c_line(2)]))
    assert pump(ctrl, lambda: store.stats.received == 2)
    ctrl.stop_session()
    assert good.calls == ["open", 1, 2, "close"]


def test_controller_rejects_bad_time():
    ctrl = MissionController(TelemetryStore())
    with pytest.raises(ValueError):
        ctrl.set_time("99:00:00")


def test_controller_new_session_clears_store():
    store = TelemetryStore()
    ctrl = MissionController(store)
    ctrl.start_session(lambda q: ScriptedSource(q, [c_line(1)]))
    assert pump(ctrl, lambda: store.stats.received == 1)
    ctrl.start_session(lambda q: ScriptedSource(q, []))
    assert store.stats.received == 0
    ctrl.stop_session()


def test_simulation_end_to_end_with_fake_cansat():
    store = TelemetryStore()
    ctrl = MissionController(store, sim_period=0.2)
    ctrl.start_session(lambda q: FakeLineSource(q, seed=1, period=0.01))
    try:
        assert pump(ctrl, lambda: ctrl.source_state is SourceState.CONNECTED)
        assert ctrl.set_telemetry(True)
        ctrl.simulation.load([101325, 95000] + [95000] * 30)
        assert ctrl.simulation.enable() and ctrl.simulation.activate()
        ok = pump(
            ctrl,
            lambda: ctrl.simulation.confirmed and store.last_container.altitude > 500,
            timeout=5,
        )
        assert ok, store.last_container
        assert store.last_container.cmd_echo.startswith("SIMP")
    finally:
        ctrl.stop_session()
    assert ctrl.simulation.state is SimState.IDLE

