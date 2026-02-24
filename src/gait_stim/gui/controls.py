from __future__ import annotations
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QDoubleSpinBox
from ..core.bus import Bus

class Controls(QWidget):
    def __init__(self, bus: Bus) -> None:
        super().__init__()
        self.bus = bus
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Manual Ψ"))
        self.psi = QDoubleSpinBox()
        self.psi.setRange(-1.0, 1.0)
        self.psi.setSingleStep(0.05)
        self.psi.valueChanged.connect(self._on_psi)
        layout.addWidget(self.psi)

    def _on_psi(self, v: float) -> None:
        self.bus.publish("gui.psi", float(v))
