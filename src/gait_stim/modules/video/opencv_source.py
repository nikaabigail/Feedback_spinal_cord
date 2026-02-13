from __future__ import annotations
import time
import cv2
from ...core.plugin import register_plugin
from ...core.config import Config
from ...core.types import VideoFrame

@register_plugin("video", "opencv")
class OpenCVVideoSource:
    def __init__(self, cfg: Config) -> None:
        cam = int(cfg.get("video", "camera_index", default=0))
        self.cap = cv2.VideoCapture(cam)
        w = cfg.get("video", "width", default=None)
        h = cfg.get("video", "height", default=None)
        if w: self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(w))
        if h: self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(h))
        self.frame_id = 0

    def get_frame(self) -> VideoFrame:
        ok, frame = self.cap.read()
        if not ok:
            raise RuntimeError("OpenCVVideoSource - не удалось получить кадр с камеры")
        ts = time.time()
        vf = VideoFrame(ts=ts, frame_id=self.frame_id, image=frame, camera_id=0)
        self.frame_id += 1
        return vf
