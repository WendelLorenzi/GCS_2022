"""Builds the application: wires store, controller, sinks and the main window."""

from __future__ import annotations

import logging
import sys
from collections.abc import Sequence

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

from gcs.config import Config
from gcs.core import MissionController, TelemetryStore
from gcs.mqtt import MqttPublisher
from gcs.persistence import CsvFlightWriter
from gcs.ui.log_console import QueueLogHandler
from gcs.ui.main_window import MainWindow


def apply_dark_theme(app: QApplication) -> None:
    app.setStyle("Fusion")
    pal = QPalette()
    base, alt, text = QColor("#1e1e1e"), QColor("#2a2a2a"), QColor("#e5e5e5")
    for role, color in (
        (QPalette.ColorRole.Window, base),
        (QPalette.ColorRole.WindowText, text),
        (QPalette.ColorRole.Base, QColor("#151515")),
        (QPalette.ColorRole.AlternateBase, alt),
        (QPalette.ColorRole.Text, text),
        (QPalette.ColorRole.Button, alt),
        (QPalette.ColorRole.ButtonText, text),
        (QPalette.ColorRole.ToolTipBase, alt),
        (QPalette.ColorRole.ToolTipText, text),
        (QPalette.ColorRole.Highlight, QColor("#2563eb")),
        (QPalette.ColorRole.HighlightedText, QColor("#ffffff")),
    ):
        pal.setColor(role, color)
    pal.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor("#6b6b6b"))
    pal.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor("#6b6b6b"))
    pal.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor("#6b6b6b"))
    app.setPalette(pal)


def build_window(cfg: Config) -> MainWindow:
    """Create every component and the window (QApplication must already exist)."""
    handler = QueueLogHandler()
    root = logging.getLogger()
    root.addHandler(handler)
    if root.level > logging.INFO or root.level == logging.NOTSET:
        root.setLevel(logging.INFO)  # the terminal must show INFO events
    store = TelemetryStore(cfg.plot_window)
    writer = CsvFlightWriter(cfg.output_dir, cfg.team_id)
    publisher = MqttPublisher(cfg.mqtt)
    controller = MissionController(
        store, sinks=[writer, publisher], team_id=cfg.team_id, sim_period=cfg.sim_period
    )
    return MainWindow(cfg, controller, writer, publisher, handler)


def run(cfg: Config, argv: Sequence[str] | None = None) -> int:
    app = QApplication(list(argv) if argv is not None else sys.argv[:1])
    app.setApplicationName("LtSat GCS")
    apply_dark_theme(app)
    window = build_window(cfg)
    window.show()
    return app.exec()
