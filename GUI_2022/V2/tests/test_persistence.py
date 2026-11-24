import datetime as dt
import queue
import time
from pathlib import Path

import pytest

from gcs.core import MissionController, TelemetryStore
from gcs.persistence import CsvFlightWriter
from gcs.protocol.telemetry import CONTAINER_HEADER, PAYLOAD_HEADER, parse_line
from gcs.transport import FakeLineSource, LineReceived, ReplayLineSource, SourceState

C1 = "1038,10:00:00.00,1,C,F,N,100.0,25.0,7.50,10:00:00,37.1966,-80.5786,710.0,8,ASCENT,CXON"
T2 = "1038,10:00:00.25,2,T,90.0,24.0,7.40,1,2,3,0,0,9.8,0.1,0.2,-0.4,12.5,TARGET_POINTING"
C3 = C1.replace(",1,C,", ",3,C,")
OFFICIAL = Path(__file__).resolve().parents[2] / "datasets"  # GUI_2022/datasets


def fixed_now():
    return dt.datetime(2022, 6, 11, 9, 30, 0)


def read(path):
    return path.read_text(encoding="utf-8").splitlines()


def test_writes_official_files_with_header(tmp_path):
    w = CsvFlightWriter(tmp_path, now=fixed_now)
    w.open_session()
    for line in (C1, T2, C3):
        w.on_packet(parse_line(line))
    c_path, t_path = w.paths
    # flushed per line: readable before close
    assert read(c_path) == [",".join(CONTAINER_HEADER), C1, C3]
    w.close_session()
    assert c_path.parent == tmp_path / "20220611_093000"
    assert c_path.name == "Flight_1038_C.csv" and t_path.name == "Flight_1038_T.csv"
    assert read(t_path) == [",".join(PAYLOAD_HEADER), T2]
    assert w.rows_written == {"C": 2, "T": 1}


@pytest.mark.skipif(not OFFICIAL.exists(), reason="legacy datasets folder not present")
def test_header_matches_competition_template(tmp_path):
    w = CsvFlightWriter(tmp_path)
    w.open_session()
    w.close_session()
    for mine, ref in zip(w.paths, ("flight_1038_C.csv", "flight_1038_T.csv")):
        official = (OFFICIAL / ref).read_text(encoding="utf-8-sig").splitlines()[0]
        assert read(mine)[0] == official


def test_never_overwrites_previous_session(tmp_path):
    w = CsvFlightWriter(tmp_path, now=fixed_now)
    w.open_session()
    w.on_packet(parse_line(C1))
    first = w.paths
    w.close_session()
    w.open_session()  # same timestamp
    w.close_session()
    assert w.session_dir.name == "20220611_093000_2"
    assert read(first[0])[1] == C1


def test_packets_outside_session_are_ignored(tmp_path, caplog):
    w = CsvFlightWriter(tmp_path)
    w.on_packet(parse_line(C1))
    w.on_packet(parse_line(C1))
    assert caplog.text.count("NOT being recorded") == 1
    assert not any(tmp_path.iterdir())


def test_disabled_writer_records_nothing(tmp_path, caplog):
    w = CsvFlightWriter(tmp_path)
    w.enabled = False
    w.open_session()
    w.on_packet(parse_line(C1))
    w.close_session()
    assert not w.recording and w.paths is None
    assert not any(tmp_path.iterdir())
    assert "NOT being recorded" not in caplog.text


def test_copy_to_usb_drive(tmp_path):
    w = CsvFlightWriter(tmp_path / "flights", now=fixed_now)
    with pytest.raises(RuntimeError):
        w.copy_to(tmp_path / "usb")  # nothing recorded
    w.open_session()
    w.on_packet(parse_line(C1))
    with pytest.raises(RuntimeError):
        w.copy_to(tmp_path / "usb")  # still recording
    w.close_session()
    copied = w.copy_to(tmp_path / "usb")
    assert [p.name for p in copied] == ["Flight_1038_C.csv", "Flight_1038_T.csv"]
    assert read(copied[0])[1] == C1
    with pytest.raises(FileExistsError):
        w.copy_to(tmp_path / "usb")
    w.copy_to(tmp_path / "usb", overwrite=True)


def test_record_and_replay_roundtrip(tmp_path):
    """Fake flight -> controller -> CSV -> ReplayLineSource reproduces the same lines."""
    store = TelemetryStore()
    writer = CsvFlightWriter(tmp_path)
    ctrl = MissionController(store, sinks=[writer])
    ctrl.start_session(lambda q: FakeLineSource(q, seed=3, telemetry_on=True, time_scale=20, period=0.01))
    deadline = time.monotonic() + 8
    while time.monotonic() < deadline and store.stats.received_t < 8:
        ctrl.poll()
        time.sleep(0.01)
    ctrl.stop_session()
    assert store.stats.received_t >= 8

    recorded = sorted(
        (parse_line(line).packet_count, line)
        for path in writer.paths
        for line in read(path)[1:]
    )
    assert len(recorded) == store.stats.received

    events: queue.Queue = queue.Queue()
    src = ReplayLineSource(events, writer.paths, speed=0)
    src.start()
    replayed = []
    while True:
        ev = events.get(timeout=3)
        if isinstance(ev, LineReceived):
            replayed.append(ev.text)
        elif ev.state is SourceState.STOPPED:
            break
    assert replayed == [line for _, line in recorded]
