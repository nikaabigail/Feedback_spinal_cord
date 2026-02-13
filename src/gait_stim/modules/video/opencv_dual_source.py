from __future__ import annotations
import time
import cv2
import numpy as np

from ...core.plugin import register_plugin
from ...core.config import Config
from ...core.types import VideoFrame

@register_plugin("video", "opencv_dual")
class OpenCVDualVideoSource:
    """
    MVP: один физический источник (камера/видео), но два логических потока:
    control и experimental. НИЧЕГО не открываем два раза.
    """
    def __init__(self, cfg: Config) -> None:
        cams = cfg.get("video", "cameras", default=None)
        if not cams or not isinstance(cams, list) or len(cams) < 2:
            cams = [{"name": "control", "index": 0}, {"name": "experimental", "index": 0}]

        self.names = [str(cams[0].get("name", "control")), str(cams[1].get("name", "experimental"))]
        self.index = int(cams[0].get("index", 0))  # используем только первый индекс

        w = cfg.get("video", "width", default=None)
        h = cfg.get("video", "height", default=None)

        # пробуем открыть через DSHOW (часто стабильнее MSMF)
        self.cap = cv2.VideoCapture(self.index, cv2.CAP_DSHOW)
        if w: self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(w))
        if h: self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(h))

        if not self.cap.isOpened():
            # fallback на MSMF
            self.cap = cv2.VideoCapture(self.index, cv2.CAP_MSMF)
            if w: self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(w))
            if h: self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(h))

        if not self.cap.isOpened():
            raise RuntimeError(f"OpenCVDualVideoSource: cannot open camera index={self.index}")

        self.frame_id = 0

    def get_frames(self) -> dict[str, VideoFrame]:
        ts = time.time()
        ok, frame = self.cap.read()
        if not ok or frame is None:
            raise RuntimeError(f"OpenCVDualVideoSource: Ошибка прочитать фрейм (index={self.index})")

        # делаем "experimental" чуть отличающимся (опционально): легкий сдвиг/шум
        # чтобы визуально было понятно что это два окна
        exp = frame
        try:
            exp = np.roll(frame, shift=8, axis=1)  # сдвиг вправо на 8 px
        except Exception:
            pass

        out = {
            self.names[0]: VideoFrame(ts=ts, frame_id=self.frame_id, image=frame, camera_id=0, camera_name=self.names[0]),
            self.names[1]: VideoFrame(ts=ts, frame_id=self.frame_id, image=exp,   camera_id=1, camera_name=self.names[1]),
        }

        self.frame_id += 1
        return out
