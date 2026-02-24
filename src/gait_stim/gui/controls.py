from __future__ import annotations

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QDoubleSpinBox, QPushButton, QFileDialog

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

        self.video_btn = QPushButton("Загрузить видео")
        self.video_btn.clicked.connect(self._on_pick_video)
        layout.addWidget(self.video_btn)

    def _on_psi(self, v: float) -> None:
        self.bus.publish("gui.psi", float(v))

    def _on_pick_video(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Выбрать видео",
            "",
            "Video Files (*.mp4 *.avi *.mov *.mkv);;All Files (*)",
        )
        if path:
            self.bus.publish("gui.video_path", path)
