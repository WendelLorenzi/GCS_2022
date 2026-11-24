"""Smoke test of the real window, headless (QT_QPA_PLATFORM=offscreen), clicking real buttons."""

import os
import time

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
QtWidgets = pytest.importorskip("PySide6.QtWidgets")

from gcs.config import Config, MqttConfig
from gcs.core import SimState
from gcs.ui.app import apply_dark_theme, build_window
from gcs.ui.main_window import SRC_FAKE, SRC_REPLAY


@pytest.fixture(scope="module")
def app():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    apply_dark_theme(app)
    return app


@pytest.fixture
def window(app, tmp_path, monkeypatch):
    # dialogs would block the test: fail loudly instead
    for name in ("warning", "critical", "information", "question"):
        monkeypatch.setattr(
            QtWidgets.QMessageBox, name,
            lambda *a, _n=name, **k: pytest.fail(f"unexpected QMessageBox.{_n}: {a[2:]}"),
        )
    cfg = Config(output_dir=tmp_path / "flights", mqtt=MqttConfig())
    w = build_window(cfg)
    w.show()
    yield w
    if w.controller.session_active:
        w.controller.stop_session()
    w.timer.stop()
    w.close()


def wait(app, cond, timeout=10.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        app.processEvents()
        if cond():
            return True
        time.sleep(0.02)
    return cond()


def test_initial_state(window):
    assert window.start_button.isEnabled()
    assert not window.stop_button.isEnabled()
    assert not window.cx_on.isEnabled()
    assert not window.copy_button.isEnabled()
    assert window.ind["conn"].text() == "Sem sessão"
    assert "GCS_MQTT_HOST" in window.mqtt_target.text()


def test_replay_mode_disables_recording(window):
    window.source_mode.setCurrentText(SRC_REPLAY)
    assert not window.record_check.isChecked()
    window.source_mode.setCurrentText(SRC_FAKE)
    assert window.record_check.isChecked()


def test_full_session_with_fake_cansat(app, window, tmp_path):
    window.source_mode.setCurrentText(SRC_FAKE)
    window.fake_scale.setValue(20)
    window.start_button.click()
    assert wait(app, lambda: window.cx_on.isEnabled())
    assert not window.start_button.isEnabled() and not window.source_mode.isEnabled()

    window.cx_on.click()
    store = window.controller.store
    assert wait(app, lambda: store.stats.received_t >= 4, timeout=15)
    assert window.ind["mission_time"].text() != "—"
    assert window.ind["last_cmd"].text() == "CMD,1038,CX,ON"
    assert int(window.ind["packets"].text().split()[0]) == store.stats.received

    # plots received data
    def plotted():
        xs = window.plots._curves[0][1].getData()[0]
        return xs is not None and len(xs) > 0

    assert wait(app, plotted)

    # simulation mode through the buttons
    profile = tmp_path / "p.txt"
    profile.write_text("CMD,$,SIMP,101325\n" * 3)
    window.controller.simulation.load_file(profile)
    window.sim_enable.click()
    assert window.controller.simulation.state is SimState.ENABLED
    assert wait(app, lambda: window.sim_activate.isEnabled())
    window.sim_activate.click()
    assert wait(app, lambda: window.controller.simulation.confirmed, timeout=5)
    assert "MODE=S" in window.sim_status.text()
    window.sim_disable.click()

    window.stop_button.click()
    assert not window.controller.session_active
    assert window.start_button.isEnabled() and window.copy_button.isEnabled()
    c_csv, _ = window.writer.paths
    assert c_csv.exists() and len(c_csv.read_text().splitlines()) > 1
    assert "Salvo" in window.flight_label.text()


def test_terminal_shows_logs(app, window):
    import logging

    logging.getLogger("gcs.test").warning("mensagem de teste")
    assert wait(app, lambda: "mensagem de teste" in window.console.toPlainText())
