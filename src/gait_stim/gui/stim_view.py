# src/gait_stim/gui/stim_view.py
from __future__ import annotations

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame
)
import pyqtgraph as pg

from ..core.types import StimParams
from ..modules.stim.waveforms import preview_wave


class ChannelPanel(QFrame):
    def __init__(self, ch_index: int) -> None:
        super().__init__()
        self.ch_index = ch_index
        self.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(6)

        self.header = QLabel(f"Ch {ch_index}")
        self.header.setStyleSheet("font-weight: 600;")
        layout.addWidget(self.header)

        self.plot = pg.PlotWidget()
        self.plot.setMenuEnabled(False)
        self.plot.setMouseEnabled(x=False, y=False)
        self.plot.showGrid(x=True, y=True, alpha=0.2)
        self.plot.setMinimumHeight(110)

        self.curve = self.plot.plot([], [])
        layout.addWidget(self.plot)

    def update_from(self, sp: StimParams) -> None:
        ch = sp.channels[self.ch_index]

        enabled = bool(getattr(ch, "enabled", False))
        amp = float(getattr(ch, "amplitude", 0.0))
        freq = float(getattr(ch, "frequency", 0.0))
        burst = float(getattr(ch, "burst_ms", 0.0))

        wf = getattr(ch, "waveform", None)
        wf_txt = f" | {wf}" if wf else ""

        self.header.setText(
            f"Ch {self.ch_index} | {'ON' if enabled else 'OFF'} | Amp {amp:.3f} | F {freq:.1f} | Burst {burst:.1f} ms{wf_txt}"
        )

        t, y = preview_wave(ch, ms=80.0, fs=2000)
        self.curve.setData(t, y)


class StimView(QWidget):
    """Вертикальный список каналов со скроллом."""
    def __init__(self) -> None:
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(6)

        title = QLabel("Stim Monitor")
        title.setStyleSheet("font-weight: 700;")
        root.addWidget(title)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.inner = QWidget()
        self.col = QVBoxLayout(self.inner)
        self.col.setContentsMargins(6, 6, 6, 6)
        self.col.setSpacing(10)

        self.scroll.setWidget(self.inner)
        root.addWidget(self.scroll)

        self.panels: list[ChannelPanel] = []
        self._last_n = 0

    def _rebuild_col(self, n: int) -> None:
        # clear
        while self.col.count():
            item = self.col.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)

        self.panels = []

        for i in range(n):
            panel = ChannelPanel(i)
            self.panels.append(panel)
            self.col.addWidget(panel)

        self.col.addStretch(1)
        self._last_n = n

    def update_params(self, sp: StimParams) -> None:
        n = len(sp.channels)

        if n != self._last_n or len(self.panels) != n:
            self._rebuild_col(n)

        for p in self.panels:
            p.update_from(sp)
