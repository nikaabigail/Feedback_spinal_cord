from __future__ import annotations

import numpy as np

from ...core.config import Config
from ...core.plugin import register_plugin
from ...core.types import PoseFrame, VideoFrame


@register_plugin("pose", "dlc_stub")
class DeepLabCutStub:
    """Заглушка DLC: формат legs8, немного иная динамика, чем yolo_stub."""

    def __init__(self, cfg: Config) -> None:
        self.K = 8

    def infer(self, frame: VideoFrame) -> PoseFrame:
        h, w = frame.image.shape[:2]
        t = frame.frame_id / 12.0

        cx, cy = w * 0.5, h * 0.58
        hip_dx = w * 0.055

        swing = np.sin(t) * (w * 0.028)
        lift = (np.sin(t * 1.2) * 0.5 + 0.5) * (h * 0.025)

        l_hip = (cx - hip_dx, cy)
        l_knee = (cx - hip_dx + swing, cy + h * 0.1)
        l_ankle = (cx - hip_dx + swing * 1.1, cy + h * 0.23 - lift)
        l_toe = (cx - hip_dx + swing * 1.4 + w * 0.028, cy + h * 0.25 - lift)

        swing2 = np.sin(t + np.pi) * (w * 0.028)
        lift2 = (np.sin((t + np.pi) * 1.2) * 0.5 + 0.5) * (h * 0.025)

        r_hip = (cx + hip_dx, cy)
        r_knee = (cx + hip_dx + swing2, cy + h * 0.1)
        r_ankle = (cx + hip_dx + swing2 * 1.1, cy + h * 0.23 - lift2)
        r_toe = (cx + hip_dx + swing2 * 1.4 + w * 0.028, cy + h * 0.25 - lift2)

        kxy = np.array([l_hip, l_knee, l_ankle, l_toe, r_hip, r_knee, r_ankle, r_toe], dtype=np.float32)
        conf = np.ones((self.K,), dtype=np.float32) * 0.92

        return PoseFrame(
            ts=frame.ts,
            frame_id=frame.frame_id,
            keypoints_xy=kxy,
            keypoints_conf=conf,
            meta={"backend": "dlc_stub", "format": "legs8"},
        )
