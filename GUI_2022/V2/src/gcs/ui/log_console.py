"""Terminal widget fed by the ``logging`` module.

Records can come from any thread (serial, paho...). The handler only enqueues them; the
widget drains the queue from the main thread (``drain()`` is called by the UI timer).
"""

from __future__ import annotations

import html
import logging
import queue

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QPlainTextEdit

_COLORS = {
    logging.DEBUG: "#8a8a8a",
    logging.INFO: "#4ade80",
    logging.WARNING: "#facc15",
    logging.ERROR: "#f87171",
    logging.CRITICAL: "#f87171",
}


class QueueLogHandler(logging.Handler):
    def __init__(self, level: int = logging.INFO) -> None:
        super().__init__(level)
        self.records: queue.SimpleQueue[tuple[int, str]] = queue.SimpleQueue()
        self.setFormatter(logging.Formatter("%(asctime)s %(message)s", "%H:%M:%S"))

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.records.put((record.levelno, self.format(record)))
        except Exception:  # noqa: BLE001 - logging must never raise
            self.handleError(record)


class LogConsole(QPlainTextEdit):
    def __init__(self, handler: QueueLogHandler, max_lines: int = 2000) -> None:
        super().__init__()
        self._handler = handler
        self.setReadOnly(True)
        self.setMaximumBlockCount(max_lines)
        self.setFont(QFont("Consolas", 9))
        self.setStyleSheet("QPlainTextEdit { background: #0b0b0b; border: 1px solid #333; }")

    def drain(self, limit: int = 200) -> None:
        for _ in range(limit):
            try:
                level, text = self._handler.records.get_nowait()
            except queue.Empty:
                return
            color = _COLORS.get(level, "#dddddd")
            self.appendHtml(f'<span style="color:{color}">{html.escape(text)}</span>')
