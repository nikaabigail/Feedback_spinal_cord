from __future__ import annotations
import numpy as np
from ...core.plugin import register_plugin
from ...core.config import Config
from ...core.types import PoseFrame, KinematicsFrame

@register_plugin("kin", "simple_kin")
class SimpleKinematics:
    """
    Пока что фейковые признаки, чтобы просто прогнать Ψ->controller.
    Потом заменю на реальные углы/события шага, возьмем из позы 2-3 ключевые точки (бедро, колено, голеностоп) и посчитаем угол в колене, амплитуду шага и длительность шага.
    """
    def __init__(self, cfg: Config) -> None:
        pass

    def compute(self, pose: PoseFrame) -> KinematicsFrame:
        # псевдо угол как функция положения точки 0
        x0, y0 = pose.keypoints_xy[0]
        angle = float(np.arctan2(y0, x0))
        feats = {"knee_angle": angle, "step_amp": abs(angle), "step_dur": 0.5}
        events = {"step": False}
        return KinematicsFrame(ts=pose.ts, frame_id=pose.frame_id, features=feats, events=events)
