"""Real serial link (LaunchPad USB) with automatic reconnection.

``port`` accepts anything ``serial.serial_for_url`` understands:
``COM5``, ``/dev/ttyACM0``, ``socket://localhost:7777`` (tools/fake_cansat.py --tcp),
``loop://`` (tests).
"""

from __future__ import annotations

import logging
import queue
import threading
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import serial
from serial.tools import list_ports

from gcs.transport.base import LineAssembler, LineSource, SourceEvent, SourceState

log = logging.getLogger(__name__)

SerialFactory = Callable[..., Any]


@dataclass(frozen=True, slots=True)
class PortInfo:
    device: str
    description: str


def list_serial_ports() -> list[PortInfo]:
    return [PortInfo(p.device, p.description) for p in sorted(list_ports.comports())]


class SerialLineSource(LineSource):
    can_send = True

    def __init__(
        self,
        events: queue.Queue[SourceEvent],
        port: str,
        baudrate: int = 9600,
        reconnect_interval: float = 1.0,
        read_timeout: float = 0.1,
        serial_factory: SerialFactory = serial.serial_for_url,
    ) -> None:
        super().__init__(events, name=f"serial:{port}")
        self.port = port
        self.baudrate = baudrate
        self.reconnect_interval = reconnect_interval
        self.read_timeout = read_timeout
        self._factory = serial_factory
        self._serial: Any = None
        self._lock = threading.Lock()

    @property
    def connected(self) -> bool:
        return self._serial is not None

    def send(self, line: str) -> None:
        if not line.endswith("\n"):
            line += "\n"
        with self._lock:
            if self._serial is None:
                raise ConnectionError(f"{self.port} is not connected")
            self._serial.write(line.encode("ascii"))
            self._serial.flush()
        log.info("[%s] sent %s", self.name, line.strip())

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                ser = self._factory(self.port, baudrate=self.baudrate, timeout=self.read_timeout)
            except (serial.SerialException, OSError, ValueError) as exc:
                self._emit_status(SourceState.DISCONNECTED, f"open failed: {exc}")
                self._stop.wait(self.reconnect_interval)
                continue

            with self._lock:
                self._serial = ser
            self._emit_status(SourceState.CONNECTED, f"{self.port} @ {self.baudrate}")
            assembler = LineAssembler()
            try:
                while not self._stop.is_set():
                    data = ser.read(ser.in_waiting or 1)
                    for text in assembler.feed(data):
                        self._emit_line(text)
            except (serial.SerialException, OSError) as exc:
                self._emit_status(SourceState.DISCONNECTED, f"read failed: {exc}")
            finally:
                with self._lock:
                    self._serial = None
                try:
                    ser.close()
                except (serial.SerialException, OSError):
                    pass
            if not self._stop.is_set():
                self._stop.wait(self.reconnect_interval)
