# src/gait_stim/gui/app.py
from __future__ import annotations

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSplitter, QSizePolicy
)
import pyqtgraph as pg

from ..core.bus import Bus
from ..core.config import Config
from ..core.pipeline import Pipeline

from .controls import Controls
from .stim_view import StimView
from .video_view import VideoView, draw_pose


class ImuView(QWidget):
    """Черновой IMU-график для двух потоков видео."""

    def __init__(self) -> None:
        super().__init__()
        self._max_len = 200
        self.ctrl: list[float] = []
        self.exp: list[float] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        title = QLabel("IMU (draft): control / experimental")
        title.setStyleSheet("font-weight: 600;")
        layout.addWidget(title)

        self.plot = pg.PlotWidget()
        self.plot.setMenuEnabled(False)
        self.plot.showGrid(x=True, y=True, alpha=0.2)
        self.plot.addLegend()
        self.curve_ctrl = self.plot.plot([], [], pen=pg.mkPen("#4caf50", width=2), name="control")
        self.curve_exp = self.plot.plot([], [], pen=pg.mkPen("#ff9800", width=2), name="experimental")
        layout.addWidget(self.plot)

    def update_control(self, v: float) -> None:
        self.ctrl.append(float(v))
        self.ctrl = self.ctrl[-self._max_len:]
        self._refresh()

    def update_experimental(self, v: float) -> None:
        self.exp.append(float(v))
        self.exp = self.exp[-self._max_len:]
        self._refresh()

    def _refresh(self) -> None:
        self.curve_ctrl.setData(range(len(self.ctrl)), self.ctrl)
        self.curve_exp.setData(range(len(self.exp)), self.exp)


class App(QWidget):
    def __init__(self, cfg_path: str) -> None:
        super().__init__()
        self.setWindowTitle("Gait-Stim MVP")

        cfg = Config.load(cfg_path)
        self.bus = Bus()
        self.pipeline = Pipeline(cfg, bus=self.bus)

        self.video_control = VideoView()
        self.video_experimental = VideoView()
        self.video_control.setMaximumHeight(420)
        self.video_experimental.setMaximumHeight(420)
        self.video_control.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.video_experimental.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.stim = StimView()
        self.imu = ImuView()
        self.controls = Controls(self.bus)

        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(6, 6, 6, 6)
        left_layout.setSpacing(8)

        cams_row = QHBoxLayout()
        cams_row.setSpacing(8)

        col1 = QVBoxLayout()
        col1.addWidget(QLabel("Control"))
        col1.addWidget(self.video_control)
        cams_row.addLayout(col1, 1)

        col2 = QVBoxLayout()
        col2.addWidget(QLabel("Experimental"))
        col2.addWidget(self.video_experimental)
        cams_row.addLayout(col2, 1)

        left_layout.addLayout(cams_row, 0)
        left_layout.addWidget(self.controls, 0)
        left_layout.addStretch(1)

        right_split = QSplitter(Qt.Orientation.Vertical)
        right_split.addWidget(self.stim)
        right_split.addWidget(self.imu)
        right_split.setStretchFactor(0, 4)
        right_split.setStretchFactor(1, 1)
        right_split.setSizes([800, 200])

        root_split = QSplitter(Qt.Orientation.Horizontal)
        root_split.addWidget(left)
        root_split.addWidget(right_split)
        root_split.setStretchFactor(0, 1)
        root_split.setStretchFactor(1, 1)
        root_split.setSizes([900, 900])

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(root_split)

        self.last_img_control = None
        self.last_pose_control = None
        self.last_img_experimental = None
        self.last_pose_experimental = None

        self.bus.subscribe("video.frame.control", self._on_video_control)
        self.bus.subscribe("pose.frame.control", self._on_pose_control)
        self.bus.subscribe("video.frame.experimental", self._on_video_experimental)
        self.bus.subscribe("pose.frame.experimental", self._on_pose_experimental)
        self.bus.subscribe("imu.value.control", self._on_imu_control)
        self.bus.subscribe("imu.value.experimental", self._on_imu_experimental)
        self.bus.subscribe("stim.params", self._on_stim)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(30)

    def _on_video_control(self, msg) -> None:
        self.last_img_control = msg.payload.image

    def _on_pose_control(self, msg) -> None:
        self.last_pose_control = msg.payload

    def _on_video_experimental(self, msg) -> None:
        self.last_img_experimental = msg.payload.image

    def _on_pose_experimental(self, msg) -> None:
        self.last_pose_experimental = msg.payload

    def _on_imu_control(self, msg) -> None:
        self.imu.update_control(msg.payload.value)

    def _on_imu_experimental(self, msg) -> None:
        self.imu.update_experimental(msg.payload.value)

    def _on_stim(self, msg) -> None:
        self.stim.update_params(msg.payload)

    def _tick(self) -> None:
        try:
            self.pipeline.step()
        except Exception as e:
            print("Pipeline error:", e)
            return

        if self.last_img_control is not None and self.last_pose_control is not None:
            img = draw_pose(
                self.last_img_control,
                self.last_pose_control.keypoints_xy,
                self.last_pose_control.keypoints_conf,
            )
            self.video_control.update_frame(img)

        if self.last_img_experimental is not None and self.last_pose_experimental is not None:
            img = draw_pose(
                self.last_img_experimental,
                self.last_pose_experimental.keypoints_xy,
                self.last_pose_experimental.keypoints_conf,
            )
            self.video_experimental.update_frame(img)


def run(cfg_path: str) -> None:
    app = QApplication([])
    w = App(cfg_path)
    w.show()
    app.exec()
