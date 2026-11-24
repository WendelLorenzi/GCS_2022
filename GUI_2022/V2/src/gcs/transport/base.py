"""Common pieces for every line source: events, line framing and the LineSource base class.

A LineSource runs in its own daemon thread and only *delivers raw text lines* to a
``queue.Queue``. It never parses telemetry and never touches the UI.
"""

from __future__ import annotations

import enum
import logging
import queue
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

log = logging.getLogger(__name__)


class SourceState(enum.Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"  # temporary; serial source keeps retrying
    FINISHED = "finished"  # replay reached the end
    STOPPED = "stopped"  # thread ended (always the last event)
    ERROR = "error"  # unexpected failure; thread ended


@dataclass(frozen=True, slots=True)
class LineReceived:
    text: str
    source: str
    timestamp: float = field(default_factory=time.time)


@dataclass(frozen=True, slots=True)
class SourceStatus:
    state: SourceState
    source: str
    message: str = ""
    timestamp: float = field(default_factory=time.time)


SourceEvent = LineReceived | SourceStatus


class CommandNotSupported(RuntimeError):
    """Raised by sources that cannot transmit (e.g. replay)."""


class LineAssembler:
    """Turns an arbitrary byte stream into complete text lines.

    Handles ``\\n`` and ``\\r\\n``, lines split across reads, empty lines and garbage
    without newlines (discarded once it exceeds ``max_line``).
    """

    def __init__(self, max_line: int = 1024, encoding: str = "ascii") -> None:
        self._buf = bytearray()
        self._max_line = max_line
        self._encoding = encoding
        self.discarded_bytes = 0

    def feed(self, data: bytes) -> list[str]:
        self._buf.extend(data)
        lines: list[str] = []
        while True:
            idx = self._buf.find(b"\n")
            if idx < 0:
                break
            raw = bytes(self._buf[:idx])
            del self._buf[: idx + 1]
            text = raw.decode(self._encoding, errors="replace").strip()
            if text:
                lines.append(text)
        if len(self._buf) > self._max_line:
            self.discarded_bytes += len(self._buf)
            log.warning("discarding %d bytes without newline", len(self._buf))
            self._buf.clear()
        return lines


class LineSource(ABC):
    """Base class: owns the worker thread and the event queue."""

    can_send: bool = False

    def __init__(self, events: queue.Queue[SourceEvent], name: str) -> None:
        self.name = name
        self._events = events
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    # -- lifecycle -------------------------------------------------------------------------
    def start(self) -> None:
        if self.running:
            return
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._run_guarded, name=f"source-{self.name}", daemon=True
        )
        self._thread.start()

    def stop(self, timeout: float = 2.0) -> None:
        self._stop.set()
        if self._thread is not None and self._thread is not threading.current_thread():
            self._thread.join(timeout)
        self._thread = None

    @property
    def running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    # -- commands --------------------------------------------------------------------------
    def send(self, line: str) -> None:
        """Transmit one command line (must end with ``\\n``)."""
        raise CommandNotSupported(f"source {self.name!r} cannot send commands")

    # -- for subclasses --------------------------------------------------------------------
    @abstractmethod
    def _run(self) -> None:
        """Worker loop. Must return promptly once ``self._stop`` is set."""

    def _emit_line(self, text: str) -> None:
        self._events.put(LineReceived(text, self.name))

    def _emit_status(self, state: SourceState, message: str = "") -> None:
        log.info("[%s] %s %s", self.name, state.value, message)
        self._events.put(SourceStatus(state, self.name, message))

    def _run_guarded(self) -> None:
        try:
            self._run()
        except Exception as exc:
            log.exception("source %s crashed", self.name)
            self._emit_status(SourceState.ERROR, repr(exc))
        finally:
            self._emit_status(SourceState.STOPPED)
