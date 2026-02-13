from __future__ import annotations
from ...core.plugin import register_plugin
from ...core.config import Config
from ...core.types import VideoFrame, PoseFrame
import numpy as np

@register_plugin("pose", "dlc_stub")
class DeepLabCutStub:
    """
    Заглушка DLC
    """
    def __init__(self, cfg: Config) -> None:
        self.K = 17

    def infer(self, frame: VideoFrame) -> PoseFrame:
        kxy = np.zeros((self.K, 2), dtype=np.float32)
        conf = np.zeros((self.K,), dtype=np.float32)
        return PoseFrame(ts=frame.ts, frame_id=frame.frame_id, keypoints_xy=kxy, keypoints_conf=conf, meta={"backend": "dlc_stub"})
