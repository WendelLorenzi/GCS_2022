"""MissionController: owns the session, the event queue and routes every packet.

Single-threaded: ``poll()`` must be called periodically from the main thread
(QTimer in the UI, a loop in the console monitor). Sources only touch ``self.events``.

    line --parse--> TelemetryStore
                 └-> SimulationRunner.on_packet
                 └-> sinks (CSV writer, MQTT publisher...)
"""

from __future__ import annotations

import logging
import queue
import time
from collections.abc import Callable, Iterable
from typing import Protocol

from gcs.core.simulation import SimulationRunner
from gcs.core.store import TelemetryStore
from gcs.protocol import commands
from gcs.protocol.telemetry import TEAM_ID, Packet, ParseError, parse_line
from gcs.transport.base import (
    CommandNotSupported,
    LineReceived,
    LineSource,
    SourceEvent,
    SourceState,
    SourceStatus,
)

log = logging.getLogger(__name__)

SourceFactory = Callable[["queue.Queue[SourceEvent]"], LineSource]


class PacketSink(Protocol):
    """Anything that consumes valid packets during a session (CSV writer, MQTT...)."""

    def open_session(self) -> None: ...
    def on_packet(self, packet: Packet) -> None: ...
    def close_session(self) -> None: ...


class MissionController:
    def __init__(
        self,
        store: TelemetryStore,
        sinks: Iterable[PacketSink] = (),
        team_id: int = TEAM_ID,
        sim_period: float = 1.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.store = store
        self.sinks = list(sinks)
        self.team_id = team_id
        self.events: queue.Queue[SourceEvent] = queue.Queue()
        self.simulation = SimulationRunner(self.send_command, team_id, sim_period, clock)
        self.source: LineSource | None = None
        self.source_state: SourceState | None = None
        self.source_message = ""
        self.last_command = ""

    @property
    def session_active(self) -> bool:
        return self.source is not None

    # -- session ---------------------------------------------------------------------------
    def start_session(self, factory: SourceFactory) -> None:
        """START: clear data, open sinks and start a new source on our event queue."""
        if self.session_active:
            self.stop_session()
        self.store.clear()
        self.source_state, self.source_message = None, ""
        for sink in self.sinks:
            self._call_sink(sink, "open_session")
        self.source = factory(self.events)
        log.info("session started (%s)", self.source.name)
        self.source.start()

    def stop_session(self) -> None:
        """STOP and Save: stop the source, process what is still queued, close sinks."""
        if self.source is None:
            return
        self.simulation.halt()
        self.source.stop()
        self.poll(max_events=None)
        self.source = None
        for sink in self.sinks:
            self._call_sink(sink, "close_session")
        s = self.store.stats
        log.info(
            "session stopped: %d packets (C=%d T=%d), %d invalid, %d lost",
            s.received, s.received_c, s.received_t, s.invalid, s.lost,
        )

    # -- main-thread pump ------------------------------------------------------------------
    def poll(self, max_events: int | None = 1000) -> int:
        """Process queued events (bounded so the UI never freezes). Returns how many."""
        n = 0
        while max_events is None or n < max_events:
            try:
                event = self.events.get_nowait()
            except queue.Empty:
                break
            n += 1
            if isinstance(event, LineReceived):
                self._handle_line(event.text)
            else:
                self._handle_status(event)
        self.simulation.tick()
        return n

    def _handle_line(self, text: str) -> None:
        try:
            packet = parse_line(text, self.team_id)
        except ParseError as exc:
            self.store.add_invalid()
            log.warning("invalid line (%s): %s", exc, text)
            return
        self.store.add(packet)
        self.simulation.on_packet(packet)
        for sink in self.sinks:
            self._call_sink(sink, "on_packet", packet)

    def _handle_status(self, event: SourceStatus) -> None:
        self.source_state = event.state
        self.source_message = event.message

    def _call_sink(self, sink: PacketSink, method: str, *args: object) -> None:
        try:
            getattr(sink, method)(*args)
        except Exception:  # a broken sink must never stop telemetry reception
            log.exception("sink %s.%s failed", type(sink).__name__, method)

    # -- commands --------------------------------------------------------------------------
    def send_command(self, line: str) -> bool:
        if self.source is None:
            log.warning("command not sent (no active session): %s", line.strip())
            return False
        try:
            self.source.send(line)
        except (ConnectionError, CommandNotSupported, OSError) as exc:
            log.warning("command not sent (%s): %s", exc, line.strip())
            return False
        self.last_command = line.strip()
        return True

    def set_telemetry(self, on: bool) -> bool:
        return self.send_command(commands.cx(on, self.team_id))

    def set_time(self, utc: str) -> bool:
        """``hh:mm:ss`` or ``GPS``. Raises ValueError for malformed input."""
        return self.send_command(commands.st(utc, self.team_id))
