"""Line sources: real serial port, CSV replay, fake CanSat.

Every source runs a daemon thread and puts ``LineReceived`` / ``SourceStatus`` events on a
``queue.Queue``. Parsing happens later, in the consumer (core).
"""

from gcs.transport.base import (
    CommandNotSupported,
    LineAssembler,
    LineReceived,
    LineSource,
    SourceEvent,
    SourceState,
    SourceStatus,
)
from gcs.transport.fake import FakeCanSat, FakeLineSource
from gcs.transport.replay import ReplayLineSource
from gcs.transport.serial_source import PortInfo, SerialLineSource, list_serial_ports

__all__ = [
    "CommandNotSupported",
    "FakeCanSat",
    "FakeLineSource",
    "LineAssembler",
    "LineReceived",
    "LineSource",
    "PortInfo",
    "ReplayLineSource",
    "SerialLineSource",
    "SourceEvent",
    "SourceState",
    "SourceStatus",
    "list_serial_ports",
]
