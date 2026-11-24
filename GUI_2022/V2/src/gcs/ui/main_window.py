"""Main window: controls (left), 8 plots (right), log terminal (bottom). Layout from PDR slide 143.

The window owns no logic: every action calls MissionController / CsvFlightWriter /
MqttPublisher. A single QTimer pumps ``controller.poll()`` and refreshes the screen.
"""

from __future__ import annotations

import datetime as dt
import logging
import time
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QCloseEvent, QFont
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from gcs.config import Config
from gcs.core import MissionController, SimState
from gcs.mqtt import MqttPublisher
from gcs.persistence import CsvFlightWriter
from gcs.transport import (
    FakeLineSource,
    ReplayLineSource,
    SerialLineSource,
    SourceState,
    list_serial_ports,
)
from gcs.ui.log_console import LogConsole, QueueLogHandler
from gcs.ui.plots import PlotPanel

log = logging.getLogger(__name__)

SRC_SERIAL, SRC_REPLAY, SRC_FAKE = "Serial (LaunchPad)", "Replay de CSV", "CanSat simulado"
BAUDS = ("9600", "19200", "38400", "57600", "115200")
PLOT_INTERVAL = 0.2  # s; plots redraw at most 5x/s, indicators every tick

_STATE_STYLE = {
    SourceState.CONNECTED: ("Conectado", "#22c55e"),
    SourceState.DISCONNECTED: ("Desconectado (tentando)", "#ef4444"),
    SourceState.FINISHED: ("Replay terminado", "#facc15"),
    SourceState.STOPPED: ("Parado", "#a3a3a3"),
    SourceState.ERROR: ("Erro", "#ef4444"),
}


def _button(text: str, color: str | None = None) -> QPushButton:
    b = QPushButton(text)
    b.setMinimumHeight(30)
    if color:
        b.setStyleSheet(
            f"QPushButton {{ background:{color}; color:white; font-weight:bold; }}"
            "QPushButton:disabled { background:#3f3f3f; color:#777; }"
        )
    return b


class MainWindow(QMainWindow):
    def __init__(
        self,
        cfg: Config,
        controller: MissionController,
        writer: CsvFlightWriter,
        publisher: MqttPublisher,
        log_handler: QueueLogHandler,
    ) -> None:
        super().__init__()
        self.cfg = cfg
        self.controller = controller
        self.store = controller.store
        self.writer = writer
        self.publisher = publisher
        self._replay_files: list[str] = []
        self._plot_version = -1
        self._last_plot = 0.0

        self.setWindowTitle(f"LtSat GCS — Team {cfg.team_id}")
        self.resize(1500, 900)

        self.plots = PlotPanel()
        self.console = LogConsole(log_handler)

        controls = QWidget()
        col = QVBoxLayout(controls)
        title = QLabel(f"LtSat GCS · Team {cfg.team_id}")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color:#ef4444;")
        col.addWidget(title)
        for group in (
            self._build_source_group(),
            self._build_session_group(),
            self._build_status_group(),
            self._build_command_group(),
            self._build_simulation_group(),
            self._build_mqtt_group(),
        ):
            col.addWidget(group)
        col.addStretch(1)

        scroll = QScrollArea()
        scroll.setWidget(controls)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setMinimumWidth(370)
        scroll.setMaximumWidth(440)

        right = QSplitter(Qt.Orientation.Vertical)
        right.addWidget(self.plots)
        right.addWidget(self.console)
        right.setStretchFactor(0, 5)
        right.setStretchFactor(1, 1)

        main = QSplitter(Qt.Orientation.Horizontal)
        main.addWidget(scroll)
        main.addWidget(right)
        main.setStretchFactor(1, 1)
        self.setCentralWidget(main)

        self._refresh_ports()
        self._on_source_mode_changed()
        self._refresh()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(cfg.ui_refresh_ms)

    # ======================================================================================
    # UI construction
    # ======================================================================================
    def _build_source_group(self) -> QGroupBox:
        box = QGroupBox("Fonte de dados")
        lay = QVBoxLayout(box)
        self.source_mode = QComboBox()
        self.source_mode.addItems([SRC_SERIAL, SRC_REPLAY, SRC_FAKE])
        self.source_mode.currentIndexChanged.connect(self._on_source_mode_changed)
        lay.addWidget(self.source_mode)

        self.source_stack = QStackedWidget()
        # serial
        w = QWidget()
        g = QGridLayout(w)
        g.setContentsMargins(0, 0, 0, 0)
        self.port_combo = QComboBox()
        self.port_combo.setEditable(True)
        self.port_combo.setToolTip("COMx, /dev/ttyACM0 ou URL pyserial (ex.: socket://localhost:7777)")
        self.port_refresh = QPushButton("↻")
        self.port_refresh.setFixedWidth(32)
        self.port_refresh.setToolTip("Atualizar lista de portas")
        self.port_refresh.clicked.connect(self._refresh_ports)
        self.baud_combo = QComboBox()
        self.baud_combo.setEditable(True)
        self.baud_combo.addItems(BAUDS)
        self.baud_combo.setCurrentText(str(self.cfg.baudrate))
        g.addWidget(QLabel("Porta"), 0, 0)
        g.addWidget(self.port_combo, 0, 1)
        g.addWidget(self.port_refresh, 0, 2)
        g.addWidget(QLabel("Baud"), 1, 0)
        g.addWidget(self.baud_combo, 1, 1, 1, 2)
        self.source_stack.addWidget(w)
        # replay
        w = QWidget()
        g = QGridLayout(w)
        g.setContentsMargins(0, 0, 0, 0)
        self.replay_button = QPushButton("Escolher CSVs…")
        self.replay_button.clicked.connect(self._choose_replay_files)
        self.replay_label = QLabel("nenhum arquivo")
        self.replay_label.setWordWrap(True)
        self.replay_speed = QDoubleSpinBox()
        self.replay_speed.setRange(0, 100)
        self.replay_speed.setValue(1)
        self.replay_speed.setSuffix(" ×")
        self.replay_speed.setToolTip("0 = o mais rápido possível")
        g.addWidget(self.replay_button, 0, 0, 1, 2)
        g.addWidget(self.replay_label, 1, 0, 1, 2)
        g.addWidget(QLabel("Velocidade"), 2, 0)
        g.addWidget(self.replay_speed, 2, 1)
        self.source_stack.addWidget(w)
        # fake
        w = QWidget()
        g = QGridLayout(w)
        g.setContentsMargins(0, 0, 0, 0)
        self.fake_scale = QDoubleSpinBox()
        self.fake_scale.setRange(1, 20)
        self.fake_scale.setValue(1)
        self.fake_scale.setSuffix(" ×")
        g.addWidget(QLabel("Acelerar voo"), 0, 0)
        g.addWidget(self.fake_scale, 0, 1)
        hint = QLabel("Envie CX ON após o START para iniciar a telemetria.")
        hint.setWordWrap(True)
        hint.setStyleSheet("color:#a3a3a3;")
        g.addWidget(hint, 1, 0, 1, 2)
        self.source_stack.addWidget(w)

        lay.addWidget(self.source_stack)
        self.record_check = QCheckBox("Gravar CSV de voo")
        self.record_check.setChecked(True)
        lay.addWidget(self.record_check)
        return box

    def _build_session_group(self) -> QGroupBox:
        box = QGroupBox("Sessão")
        g = QGridLayout(box)
        self.start_button = _button("START", "#15803d")
        self.stop_button = _button("STOP and Save", "#b91c1c")
        self.copy_button = QPushButton("Copiar CSVs para pendrive…")
        self.flight_label = QLabel("")
        self.flight_label.setWordWrap(True)
        self.flight_label.setStyleSheet("color:#a3a3a3;")
        self.flight_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.start_button.clicked.connect(self._start)
        self.stop_button.clicked.connect(self._stop)
        self.copy_button.clicked.connect(self._copy_flight)
        g.addWidget(self.start_button, 0, 0)
        g.addWidget(self.stop_button, 0, 1)
        g.addWidget(self.copy_button, 1, 0, 1, 2)
        g.addWidget(self.flight_label, 2, 0, 1, 2)
        return box

    def _build_status_group(self) -> QGroupBox:
        box = QGroupBox("Estado")
        form = QFormLayout(box)
        big = QFont("Consolas", 12, QFont.Weight.Bold)
        self.ind: dict[str, QLabel] = {}
        for key, label, font in (
            ("conn", "Conexão", None),
            ("mission_time", "Mission Time", big),
            ("gps_time", "GPS Time", big),
            ("packets", "Packets Received", big),
            ("errors", "Inválidos / perdidos", None),
            ("c_state", "Estado container", None),
            ("t_state", "Estado payload", None),
            ("mode", "Modo", None),
            ("released", "Payload liberado", None),
            ("sats", "Satélites GPS", None),
            ("pointing", "Pointing error", None),
            ("echo", "CMD_ECHO", None),
            ("last_cmd", "Último comando", None),
        ):
            lbl = QLabel("—")
            lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            if font:
                lbl.setFont(font)
            self.ind[key] = lbl
            form.addRow(label, lbl)
        return box

    def _build_command_group(self) -> QGroupBox:
        box = QGroupBox("Comandos")
        g = QGridLayout(box)
        self.cx_on = _button("CX ON", "#1d4ed8")
        self.cx_off = _button("CX OFF")
        self.cx_on.clicked.connect(lambda: self.controller.set_telemetry(True))
        self.cx_off.clicked.connect(lambda: self.controller.set_telemetry(False))
        self.st_edit = QLineEdit()
        self.st_edit.setPlaceholderText("hh:mm:ss (UTC)")
        self.st_send = QPushButton("ST")
        self.st_now = QPushButton("ST UTC agora")
        self.st_gps = QPushButton("ST GPS")
        self.st_send.clicked.connect(self._send_time)
        self.st_edit.returnPressed.connect(self._send_time)
        self.st_now.clicked.connect(
            lambda: self.controller.set_time(dt.datetime.now(dt.timezone.utc).strftime("%H:%M:%S"))
        )
        self.st_gps.clicked.connect(lambda: self.controller.set_time("GPS"))
        g.addWidget(self.cx_on, 0, 0)
        g.addWidget(self.cx_off, 0, 1)
        g.addWidget(self.st_edit, 1, 0)
        g.addWidget(self.st_send, 1, 1)
        g.addWidget(self.st_now, 2, 0)
        g.addWidget(self.st_gps, 2, 1)
        return box

    def _build_simulation_group(self) -> QGroupBox:
        box = QGroupBox("Modo simulação")
        g = QGridLayout(box)
        self.sim_load = QPushButton("Carregar perfil SIMP…")
        self.sim_load.clicked.connect(self._load_profile)
        self.sim_enable = _button("SIMULATION ENABLE", "#7c3aed")
        self.sim_activate = _button("SIMULATION ACTIVATE", "#7c3aed")
        self.sim_disable = _button("SIM DISABLE")
        self.sim_enable.clicked.connect(self.controller.simulation.enable)
        self.sim_activate.clicked.connect(self.controller.simulation.activate)
        self.sim_disable.clicked.connect(self.controller.simulation.disable)
        self.sim_status = QLabel("sem perfil")
        self.sim_status.setWordWrap(True)
        g.addWidget(self.sim_load, 0, 0, 1, 2)
        g.addWidget(self.sim_enable, 1, 0)
        g.addWidget(self.sim_activate, 1, 1)
        g.addWidget(self.sim_disable, 2, 0, 1, 2)
        g.addWidget(self.sim_status, 3, 0, 1, 2)
        return box

    def _build_mqtt_group(self) -> QGroupBox:
        box = QGroupBox("MQTT")
        g = QGridLayout(box)
        self.mqtt_enable = _button("MQTT ENABLE", "#0e7490")
        self.mqtt_disable = _button("MQTT DISABLE")
        self.mqtt_enable.clicked.connect(self._enable_mqtt)
        self.mqtt_disable.clicked.connect(self.publisher.disable)
        self.mqtt_status = QLabel()
        self.mqtt_status.setWordWrap(True)
        m = self.cfg.mqtt
        target = f"{m.host}:{m.port} · {m.topic}" if m.configured else "GCS_MQTT_HOST não definido"
        self.mqtt_target = QLabel(target)
        self.mqtt_target.setStyleSheet("color:#a3a3a3;")
        self.mqtt_target.setWordWrap(True)
        g.addWidget(self.mqtt_enable, 0, 0)
        g.addWidget(self.mqtt_disable, 0, 1)
        g.addWidget(self.mqtt_target, 1, 0, 1, 2)
        g.addWidget(self.mqtt_status, 2, 0, 1, 2)
        return box

    # ======================================================================================
    # actions
    # ======================================================================================
    def _refresh_ports(self) -> None:
        current = self.port_combo.currentText()
        self.port_combo.clear()
        for p in list_serial_ports():
            self.port_combo.addItem(p.device)
            self.port_combo.setItemData(
                self.port_combo.count() - 1, p.description, Qt.ItemDataRole.ToolTipRole
            )
        if current:
            self.port_combo.setCurrentText(current)

    def _on_source_mode_changed(self) -> None:
        self.source_stack.setCurrentIndex(self.source_mode.currentIndex())
        # replaying a recorded flight must not create a duplicate flight folder
        self.record_check.setChecked(self.source_mode.currentText() != SRC_REPLAY)

    def _choose_replay_files(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(
            self, "CSVs de voo", str(self.cfg.output_dir), "CSV (*.csv);;Todos (*)"
        )
        if files:
            self._replay_files = files
            self.replay_label.setText("\n".join(Path(f).name for f in files))

    def _start(self) -> None:
        mode = self.source_mode.currentText()
        if mode == SRC_SERIAL:
            port = self.port_combo.currentText().strip()
            try:
                baud = int(self.baud_combo.currentText())
            except ValueError:
                self._warn("Baud rate inválido.")
                return
            if not port:
                self._warn("Escolha a porta serial.")
                return

            def factory(q):
                return SerialLineSource(q, port, baudrate=baud)
        elif mode == SRC_REPLAY:
            if not self._replay_files:
                self._warn("Escolha os CSVs para o replay.")
                return
            files, speed = list(self._replay_files), self.replay_speed.value()

            def factory(q):
                return ReplayLineSource(q, files, speed=speed, team_id=self.cfg.team_id)
        else:
            scale = self.fake_scale.value()

            def factory(q):
                return FakeLineSource(q, time_scale=scale)

        self.writer.enabled = self.record_check.isChecked()
        self.plots.clear()
        self._plot_version = -1
        self.flight_label.setText("")
        self.controller.start_session(factory)
        if self.writer.recording and self.writer.session_dir:
            self._show_flight_dir("Gravando em")
        self._refresh()

    def _stop(self) -> None:
        self.controller.stop_session()
        self.plots.update_from(self.store)
        if self.writer.enabled and self.writer.session_dir:
            r = self.writer.rows_written
            self._show_flight_dir(f"Salvo ({r['C']} C / {r['T']} T) em")
        self._refresh()

    def _show_flight_dir(self, prefix: str) -> None:
        # short text (a long path would widen the panel); full path in the tooltip
        d = self.writer.session_dir
        assert d is not None
        self.flight_label.setText(f"{prefix}: {d.parent.name}/{d.name}")
        self.flight_label.setToolTip(str(d))

    def _copy_flight(self) -> None:
        dest = QFileDialog.getExistingDirectory(self, "Pasta de destino (pendrive)")
        if not dest:
            return
        try:
            try:
                copied = self.writer.copy_to(dest)
            except FileExistsError as exc:
                answer = QMessageBox.question(
                    self, "Arquivo existe", f"{exc} já existe. Sobrescrever?"
                )
                if answer != QMessageBox.StandardButton.Yes:
                    return
                copied = self.writer.copy_to(dest, overwrite=True)
        except (OSError, RuntimeError) as exc:
            QMessageBox.critical(self, "Falha ao copiar", str(exc))
            return
        QMessageBox.information(self, "Copiado", "\n".join(str(p) for p in copied))

    def _send_time(self) -> None:
        text = self.st_edit.text().strip()
        try:
            self.controller.set_time(text)
        except ValueError as exc:
            self._warn(str(exc))

    def _load_profile(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Perfil de pressão (SIMP)", "", "Perfis (*.txt *.csv);;Todos (*)"
        )
        if not path:
            return
        try:
            self.controller.simulation.load_file(path)
        except (OSError, ValueError, RuntimeError) as exc:
            QMessageBox.critical(self, "Perfil inválido", str(exc))
        self._refresh()

    def _enable_mqtt(self) -> None:
        if not self.publisher.enable():
            self._warn(f"MQTT não ligado: {self.publisher.last_error}")

    def _warn(self, text: str) -> None:
        log.warning(text)
        QMessageBox.warning(self, "LtSat GCS", text)

    # ======================================================================================
    # periodic refresh
    # ======================================================================================
    def _tick(self) -> None:
        self.controller.poll()
        self.console.drain()
        now = time.monotonic()
        if self.store.version != self._plot_version and now - self._last_plot >= PLOT_INTERVAL:
            self.plots.update_from(self.store)
            self._plot_version = self.store.version
            self._last_plot = now
        self._refresh()

    def _refresh(self) -> None:
        ctrl, store, sim = self.controller, self.store, self.controller.simulation
        active = ctrl.session_active
        connected = active and ctrl.source_state is SourceState.CONNECTED
        can_cmd = connected and ctrl.source is not None and ctrl.source.can_send

        # -- indicators
        if active or ctrl.source_state is not None:
            text, color = _STATE_STYLE.get(ctrl.source_state, ("Conectando…", "#facc15"))
            if ctrl.source_message and ctrl.source_state is not SourceState.CONNECTED:
                text += f" — {ctrl.source_message}"
        else:
            text, color = "Sem sessão", "#a3a3a3"
        self.ind["conn"].setText(text)
        self.ind["conn"].setStyleSheet(f"color:{color}; font-weight:bold;")

        c, t, s = store.last_container, store.last_payload, store.stats
        self.ind["mission_time"].setText(c.mission_time if c else (t.mission_time if t else "—"))
        self.ind["gps_time"].setText(c.gps_time if c else "—")
        self.ind["packets"].setText(f"{s.received}  (C {s.received_c} · T {s.received_t})")
        self.ind["errors"].setText(f"{s.invalid} / {s.lost}" + (f"  · resets {s.resets}" if s.resets else ""))
        self.ind["errors"].setStyleSheet("color:#facc15;" if (s.invalid or s.lost) else "")
        self.ind["c_state"].setText(c.software_state if c else "—")
        self.ind["t_state"].setText(t.tp_software_state if t else "—")
        mode = {"F": "F — voo", "S": "S — simulação"}.get(c.mode, c.mode) if c else "—"
        self.ind["mode"].setText(mode)
        self.ind["released"].setText({"N": "Não", "R": "Sim"}.get(c.tp_released, c.tp_released) if c else "—")
        self.ind["sats"].setText(str(c.gps_sats) if c and c.gps_sats is not None else "—")
        self.ind["pointing"].setText(
            f"{t.pointing_error:.1f}°" if t and t.pointing_error is not None else "—"
        )
        self.ind["echo"].setText(c.cmd_echo if c and c.cmd_echo else "—")
        self.ind["last_cmd"].setText(ctrl.last_command or "—")

        # -- simulation
        done, total = sim.progress
        if not total:
            self.sim_status.setText("sem perfil")
        else:
            confirmed = " · CanSat em MODE=S ✔" if sim.confirmed else ""
            self.sim_status.setText(
                f"{sim.profile_name}: {sim.state.value} {done}/{total}{confirmed}"
            )

        # -- mqtt
        p = self.publisher
        if not p.enabled:
            ms, mc = "desligado", "#a3a3a3"
        elif p.connected:
            ms, mc = f"conectado · enviados {p.published} · descartados {p.dropped}", "#22c55e"
        else:
            ms, mc = f"conectando… {p.last_error}".strip(), "#facc15"
        self.mqtt_status.setText(ms)
        self.mqtt_status.setStyleSheet(f"color:{mc};")

        # -- enabled states
        self.start_button.setEnabled(not active)
        self.stop_button.setEnabled(active)
        self.copy_button.setEnabled(not active and self.writer.paths is not None)
        for w in (self.source_mode, self.source_stack, self.record_check):
            w.setEnabled(not active)
        for w in (self.cx_on, self.cx_off, self.st_edit, self.st_send, self.st_now, self.st_gps):
            w.setEnabled(can_cmd)
        self.sim_load.setEnabled(sim.state is not SimState.RUNNING)
        self.sim_enable.setEnabled(can_cmd and sim.state is SimState.IDLE)
        self.sim_activate.setEnabled(can_cmd and sim.state is SimState.ENABLED and total > 0)
        self.sim_disable.setEnabled(can_cmd and sim.state is not SimState.IDLE)
        self.mqtt_enable.setEnabled(not p.enabled)
        self.mqtt_disable.setEnabled(p.enabled)

    # ======================================================================================
    def closeEvent(self, event: QCloseEvent) -> None:
        if self.controller.session_active:
            answer = QMessageBox.question(
                self, "Sessão ativa", "Há uma sessão ativa. Encerrar (STOP and Save) e sair?"
            )
            if answer != QMessageBox.StandardButton.Yes:
                event.ignore()
                return
            self.controller.stop_session()
        self.timer.stop()
        self.publisher.disable()
        self.console.drain()
        event.accept()
