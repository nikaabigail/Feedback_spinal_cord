from __future__ import annotations

import time

import cv2
import numpy as np

from ...core.bus import Bus
from ...core.config import Config
from ...core.plugin import register_plugin
from ...core.types import VideoFrame


@register_plugin("video", "opencv_dual")
class OpenCVDualVideoSource:
    """
    MVP: один физический источник (камера/видео), но два логических потока:
    control и experimental. НИЧЕГО не открываем два раза.
    """

    def __init__(self, cfg: Config, bus: Bus | None = None) -> None:
        self.bus = bus
        cams = cfg.get("video", "cameras", default=None)
        if not cams or not isinstance(cams, list) or len(cams) < 2:
            cams = [{"name": "control", "index": 0}, {"name": "experimental", "index": 0}]

        self.names = [str(cams[0].get("name", "control")), str(cams[1].get("name", "experimental"))]
        self.index = int(cams[0].get("index", 0))
        self.video_path = cfg.get("video", "path", default=None)
        self.width = cfg.get("video", "width", default=None)
        self.height = cfg.get("video", "height", default=None)

        self.cap: cv2.VideoCapture | None = None
        self._open_capture()

        if self.bus is not None:
            self.bus.subscribe("gui.video_path", self._on_video_path)

        self.frame_id = 0

    def _open_capture(self) -> None:
        if self.cap is not None:
            self.cap.release()

        if self.video_path:
            self.cap = cv2.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                raise RuntimeError(f"OpenCVDualVideoSource: cannot open video path={self.video_path}")
            return

        self.cap = cv2.VideoCapture(self.index, cv2.CAP_DSHOW)
        if self.width:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(self.width))
        if self.height:
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(self.height))

        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(self.index, cv2.CAP_MSMF)
            if self.width:
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(self.width))
            if self.height:
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(self.height))

        if not self.cap.isOpened():
            raise RuntimeError(f"OpenCVDualVideoSource: cannot open camera index={self.index}")

    def _on_video_path(self, msg) -> None:
        prev_path = self.video_path
        path = str(msg.payload).strip()
        self.video_path = path or None
        try:
            self._open_capture()
        except RuntimeError as exc:
            self.video_path = prev_path
            self._open_capture()
            print(f"OpenCVDualVideoSource: {exc}")

    def get_frames(self) -> dict[str, VideoFrame]:
        assert self.cap is not None
        ts = time.time()
        ok, frame = self.cap.read()
        if not ok or frame is None:
            if self.video_path:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ok, frame = self.cap.read()
            if not ok or frame is None:
                raise RuntimeError(f"OpenCVDualVideoSource: Ошибка прочитать фрейм (index={self.index})")

        exp = frame
        try:
            exp = np.roll(frame, shift=8, axis=1)
        except Exception:
            pass

        out = {
            self.names[0]: VideoFrame(ts=ts, frame_id=self.frame_id, image=frame, camera_id=0, camera_name=self.names[0]),
            self.names[1]: VideoFrame(ts=ts, frame_id=self.frame_id, image=exp, camera_id=1, camera_name=self.names[1]),
        }
        self.frame_id += 1
        return out
