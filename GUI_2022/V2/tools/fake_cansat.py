"""Fake CanSat over a real byte channel, to test the GCS serial path end to end.

Examples:
    # cross-platform, no drivers: GCS connects to socket://localhost:7777
    python tools/fake_cansat.py --tcp 7777

    # virtual COM pair (com0com on Windows / socat on Linux): fake on one end, GCS on the other
    python tools/fake_cansat.py --port COM11

    # just print packets
    python tools/fake_cansat.py --stdout --autostart --time-scale 5

Telemetry starts after the GCS sends ``CMD,1038,CX,ON`` (or immediately with --autostart).
"""

from __future__ import annotations

import argparse
import logging
import socket
import sys
import time
from pathlib import Path

try:
    import gcs  # noqa: F401
except ModuleNotFoundError:  # running without `pip install -e .`
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gcs.transport.base import LineAssembler
from gcs.transport.fake import FakeCanSat

log = logging.getLogger("fake_cansat")
TICK = 0.02


def _pump(cansat: FakeCanSat, read, write) -> None:
    """Run until the channel breaks. ``read()`` -> bytes (non-blocking), ``write(bytes)``."""
    assembler = LineAssembler()
    while True:
        for cmd in assembler.feed(read()):
            ok = cansat.handle_command(cmd)
            log.info("cmd %-28s %s", cmd, "ok" if ok else "REJECTED")
        for line in cansat.tick():
            write((line + "\n").encode("ascii"))
        time.sleep(TICK)


def run_tcp(cansat: FakeCanSat, port: int) -> None:
    with socket.create_server(("127.0.0.1", port)) as server:
        while True:
            log.info("waiting for GCS on socket://localhost:%d", port)
            conn, addr = server.accept()
            log.info("GCS connected from %s", addr)
            conn.setblocking(False)

            def read(conn: socket.socket = conn) -> bytes:
                try:
                    data = conn.recv(4096)
                except BlockingIOError:
                    return b""
                if not data:
                    raise ConnectionResetError("GCS closed the connection")
                return data

            try:
                _pump(cansat, read, conn.sendall)
            except OSError as exc:
                log.info("connection closed: %s", exc)
            finally:
                conn.close()


def run_serial(cansat: FakeCanSat, port: str, baud: int) -> None:
    import serial

    with serial.serial_for_url(port, baudrate=baud, timeout=0) as ser:
        log.info("fake CanSat on %s @ %d", port, baud)
        _pump(cansat, lambda: ser.read(ser.in_waiting or 1), ser.write)


def run_stdout(cansat: FakeCanSat) -> None:
    def write(data: bytes) -> None:
        sys.stdout.write(data.decode("ascii"))
        sys.stdout.flush()

    _pump(cansat, lambda: b"", write)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    out = ap.add_mutually_exclusive_group(required=True)
    out.add_argument("--tcp", type=int, metavar="PORT", help="serve on localhost:PORT")
    out.add_argument("--port", help="serial port / pyserial URL to write to")
    out.add_argument("--stdout", action="store_true", help="print packets")
    ap.add_argument("--baud", type=int, default=9600)
    ap.add_argument("--time-scale", type=float, default=1.0, help="speed up the flight profile")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--autostart", action="store_true", help="telemetry on without CX ON")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", stream=sys.stderr)
    cansat = FakeCanSat(time_scale=args.time_scale, seed=args.seed, telemetry_on=args.autostart)
    try:
        if args.tcp:
            run_tcp(cansat, args.tcp)
        elif args.port:
            run_serial(cansat, args.port, args.baud)
        else:
            run_stdout(cansat)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
