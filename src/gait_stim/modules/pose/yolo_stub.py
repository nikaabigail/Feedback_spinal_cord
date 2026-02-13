# modules/pose/yolo_stub.py
from __future__ import annotations
import numpy as np
from ...core.plugin import register_plugin
from ...core.config import Config
from ...core.types import VideoFrame, PoseFrame

@register_plugin("pose", "yolo_stub")
class YoloPoseStub:
    """
    Заглушка пока что, она генерит ключевые точки ног (L/R), чтобы
    отлаживать GUI и пайплайн без реального YOLO/DLC.
    """
    def __init__(self, cfg: Config) -> None:
        # 8 точек: L_hip, L_knee, L_ankle, L_toe, R_hip, R_knee, R_ankle, R_toe
        self.K = 8

    def infer(self, frame: VideoFrame) -> PoseFrame:
        h, w = frame.image.shape[:2]
        t = frame.frame_id / 10.0

        cx, cy = w * 0.5, h * 0.55
        hip_dx = w * 0.06

        # “шагание”: колено/голеностоп немного ходят вперед-назад
        swing = np.sin(t) * (w * 0.03)
        lift  = (np.sin(t) * 0.5 + 0.5) * (h * 0.02)

        # Левая нога
        L_hip   = (cx - hip_dx, cy)
        L_knee  = (cx - hip_dx + swing, cy + h*0.12)
        L_ankle = (cx - hip_dx + swing*1.2, cy + h*0.25 - lift)
        L_toe   = (cx - hip_dx + swing*1.4 + w*0.03, cy + h*0.27 - lift)

        # Правая нога (в противофазе)
        swing2 = np.sin(t + np.pi) * (w * 0.03)
        lift2  = (np.sin(t + np.pi) * 0.5 + 0.5) * (h * 0.02)

        R_hip   = (cx + hip_dx, cy)
        R_knee  = (cx + hip_dx + swing2, cy + h*0.12)
        R_ankle = (cx + hip_dx + swing2*1.2, cy + h*0.25 - lift2)
        R_toe   = (cx + hip_dx + swing2*1.4 + w*0.03, cy + h*0.27 - lift2)

        kxy = np.array([L_hip, L_knee, L_ankle, L_toe, R_hip, R_knee, R_ankle, R_toe], dtype=np.float32)
        conf = np.ones((self.K,), dtype=np.float32) * 0.9

        return PoseFrame(
            ts=frame.ts,
            frame_id=frame.frame_id,
            keypoints_xy=kxy,
            keypoints_conf=conf,
            meta={"backend": "yolo_stub", "format": "legs8"}
        )
