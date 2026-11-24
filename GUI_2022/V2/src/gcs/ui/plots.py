"""The 8 telemetry plots of the PDR (slide 143), drawn with pyqtgraph."""

from __future__ import annotations

from dataclasses import dataclass

import pyqtgraph as pg
from PySide6.QtWidgets import QGridLayout, QWidget

from gcs.core.store import PacketKind, TelemetryStore

RED, GREEN, BLUE = "#ef4444", "#22c55e", "#3b82f6"


@dataclass(frozen=True)
class Curve:
    kind: PacketKind
    field: str
    name: str
    color: str


@dataclass(frozen=True)
class PlotSpec:
    title: str
    y_label: str
    curves: tuple[Curve, ...]
    x_label: str = "Tempo (s)"


PLOTS: tuple[PlotSpec, ...] = (
    PlotSpec("Temperatura", "°C", (
        Curve("C", "temp", "Container", RED), Curve("T", "tp_temp", "Payload", GREEN))),
    PlotSpec("Altitude", "m", (
        Curve("C", "altitude", "Container", RED), Curve("T", "tp_altitude", "Payload", GREEN))),
    PlotSpec("Tensão", "V", (
        Curve("C", "voltage", "Container", RED), Curve("T", "tp_voltage", "Payload", GREEN))),
    PlotSpec("GPS container", "Latitude (°)", (), x_label="Longitude (°)"),  # special: lon x lat
    PlotSpec("Altitude GPS", "m (MSL)", (Curve("C", "gps_altitude", "Container", RED),)),
    PlotSpec("Giroscópio payload", "°/s", (
        Curve("T", "gyro_r", "R", RED), Curve("T", "gyro_p", "P", GREEN),
        Curve("T", "gyro_y", "Y", BLUE))),
    PlotSpec("Acelerômetro payload", "m/s²", (
        Curve("T", "accel_r", "R", RED), Curve("T", "accel_p", "P", GREEN),
        Curve("T", "accel_y", "Y", BLUE))),
    PlotSpec("Magnetômetro payload", "G", (
        Curve("T", "mag_r", "R", RED), Curve("T", "mag_p", "P", GREEN),
        Curve("T", "mag_y", "Y", BLUE))),
)


class PlotPanel(QWidget):
    def __init__(self, columns: int = 2) -> None:
        super().__init__()
        pg.setConfigOptions(antialias=True, background="#111111", foreground="#d4d4d4")
        grid = QGridLayout(self)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(4)
        self._curves: list[tuple[Curve, pg.PlotDataItem]] = []
        self._gps: pg.PlotDataItem | None = None
        self.plots: list[pg.PlotWidget] = []
        for i, spec in enumerate(PLOTS):
            w = pg.PlotWidget(title=spec.title)
            w.showGrid(x=True, y=True, alpha=0.2)
            w.setLabel("left", spec.y_label)
            w.setLabel("bottom", spec.x_label)
            w.getPlotItem().setDownsampling(auto=True, mode="peak")
            w.getPlotItem().setClipToView(True)
            for axis in ("left", "bottom"):  # no "x0.001" auto prefixes: show real units
                w.getPlotItem().getAxis(axis).enableAutoSIPrefix(False)
            if spec.curves:
                w.addLegend(offset=(-5, 5))
                for c in spec.curves:
                    item = w.plot(name=c.name, pen=pg.mkPen(c.color, width=1.5), connect="finite")
                    self._curves.append((c, item))
            else:
                # points only: at 0.0001 deg resolution a connecting line is just jitter.
                # x (longitude) is not monotonic, so clip/downsample would hide points.
                w.getPlotItem().setClipToView(False)
                w.getPlotItem().setDownsampling(auto=False)
                self._gps = w.plot(
                    pen=None, symbol="o", symbolSize=5, symbolBrush=RED, symbolPen=None
                )
            self.plots.append(w)
            grid.addWidget(w, i // columns, i % columns)

    def update_from(self, store: TelemetryStore) -> None:
        for curve, item in self._curves:
            xs, ys = store.series(curve.kind, curve.field)
            item.setData(xs, ys)
        if self._gps is not None:
            _, lat = store.series("C", "gps_latitude")
            _, lon = store.series("C", "gps_longitude")
            self._gps.setData(lon, lat)

    def clear(self) -> None:
        for _, item in self._curves:
            item.setData([], [])
        if self._gps is not None:
            self._gps.setData([], [])
