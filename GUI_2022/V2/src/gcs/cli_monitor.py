"""Headless console monitor: ``python -m gcs monitor ...``.

Runs the same MissionController as the UI, without a window. Useful on the field to check
the link quickly, or over SSH:

    python -m gcs monitor --list-ports
    python -m gcs monitor --port COM5 --cx-on
    python -m gcs monitor --port socket://localhost:7777 --cx-on     # tools/fake_cansat.py --tcp 7777
    python -m gcs monitor --fake --time-scale 5 --cx-on
    python -m gcs monitor --fake --cx-on --sim tools/sim_profile_example.txt
    python -m gcs monitor --replay flights/<sessao>/Flight_1038_C.csv flights/<sessao>/Flight_1038_T.csv --speed 10

``--mqtt`` publishes to the broker set in GCS_MQTT_* env vars (or ./.env).
Flight CSVs are recorded to ``--out`` (default ./flights/<YYYYmmdd_HHMMSS>/), except in replay.
"""

from __future__ import annotations

import argparse
import logging
import queue
import time
from pathlib import Path

from gcs.config import Config
from gcs.core import MissionController, SimState, TelemetryStore
from gcs.mqtt import MqttPublisher
from gcs.persistence import CsvFlightWriter
from gcs.protocol.telemetry import Packet
from gcs.transport import (
    FakeLineSource,
    ReplayLineSource,
    SerialLineSource,
    SourceState,
    list_serial_ports,
)
from gcs.transport.base import SourceEvent

log = logging.getLogger("gcs")


class PrintSink:
    """Console sink: one line per packet."""

    def open_session(self) -> None:
        pass

    def on_packet(self, packet: Packet) -> None:
        print(f"{packet.packet_type} #{packet.packet_count:<5} {','.join(packet.raw)}")

    def close_session(self) -> None:
        pass


def _factory(args: argparse.Namespace, cfg: Config):
    def build(events: queue.Queue[SourceEvent]):
        if args.fake:
            return FakeLineSource(events, time_scale=args.time_scale)
        if args.replay:
            return ReplayLineSource(events, args.replay, speed=args.speed, team_id=cfg.team_id)
        return SerialLineSource(events, args.port, baudrate=args.baud)

    return build


def monitor(ctrl: MissionController, args: argparse.Namespace) -> None:
    sim_started = False
    cx_sent = False
    try:
        while ctrl.session_active:
            ctrl.poll()
            state = ctrl.source_state
            if state is SourceState.CONNECTED and not cx_sent and args.cx_on:
                cx_sent = ctrl.set_telemetry(True)
            if state is SourceState.CONNECTED and args.sim and not sim_started:
                sim_started = ctrl.simulation.enable() and ctrl.simulation.activate()
            if state in (SourceState.FINISHED, SourceState.STOPPED, SourceState.ERROR):
                break
            if sim_started and ctrl.simulation.state is SimState.FINISHED:
                log.info("simulation profile done; stopping")
                break
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        ctrl.stop_session()


def main(argv: list[str] | None = None) -> None:
    cfg = Config.from_env()
    ap = argparse.ArgumentParser(prog="gcs monitor", description="LtSat GCS V2 (console monitor)")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--list-ports", action="store_true")
    src.add_argument("--port", help="COMx, /dev/ttyACM0 or pyserial URL")
    src.add_argument("--fake", action="store_true", help="in-process fake CanSat")
    src.add_argument("--replay", nargs="+", metavar="CSV")
    ap.add_argument("--baud", type=int, default=cfg.baudrate)
    ap.add_argument("--speed", type=float, default=1.0, help="replay speed (0 = max)")
    ap.add_argument("--time-scale", type=float, default=1.0, help="fake flight speed-up")
    ap.add_argument("--cx-on", action="store_true", help="send CMD,1038,CX,ON on connect")
    ap.add_argument("--sim", metavar="PROFILE", help="run simulation mode with this SIMP profile")
    ap.add_argument("--out", type=Path, default=cfg.output_dir, help="flight CSV folder")
    ap.add_argument("--no-record", action="store_true", help="do not write flight CSVs")
    ap.add_argument("--mqtt", action="store_true", help="publish telemetry via MQTT")
    args = ap.parse_args(argv)

    if args.list_ports:
        for port in list_serial_ports():
            print(f"{port.device:<15} {port.description}")
        return

    sinks: list = [PrintSink()]
    if not (args.no_record or args.replay):
        sinks.append(CsvFlightWriter(args.out, cfg.team_id))
    publisher = MqttPublisher(cfg.mqtt)
    sinks.append(publisher)
    if args.mqtt and not publisher.enable():
        ap.error(f"MQTT: {publisher.last_error}")
    ctrl = MissionController(
        TelemetryStore(cfg.plot_window), sinks=sinks, team_id=cfg.team_id,
        sim_period=cfg.sim_period,
    )
    if args.sim:
        ctrl.simulation.load_file(args.sim)
    ctrl.start_session(_factory(args, cfg))
    try:
        monitor(ctrl, args)
    finally:
        publisher.disable()
