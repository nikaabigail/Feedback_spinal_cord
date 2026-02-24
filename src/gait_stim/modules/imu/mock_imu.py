from __future__ import annotations

from ...core.plugin import register_plugin
from ...core.config import Config
from ...core.types import PoseFrame, ImuSample


@register_plugin("imu", "mock_imu")
class MockImuEstimator:
    """Черновой IMU из кинематики ног: разница высоты носков L/R."""

    def __init__(self, cfg: Config) -> None:
        self.alpha = float(cfg.get("imu", "smoothing", default=0.85))
        self._state: dict[str, float] = {}

    def compute(self, pose: PoseFrame, source: str) -> ImuSample:
        kxy = pose.keypoints_xy
        conf = pose.keypoints_conf

        # для legs8 ожидаем toe индексы 3 и 7
        raw = 0.0
        if len(kxy) >= 8 and len(conf) >= 8 and float(conf[3]) > 0.1 and float(conf[7]) > 0.1:
            raw = float(kxy[3][1] - kxy[7][1])

        prev = self._state.get(source, raw)
        filt = self.alpha * prev + (1.0 - self.alpha) * raw
        self._state[source] = filt

        return ImuSample(
            ts=pose.ts,
            frame_id=pose.frame_id,
            source=source,
            value=float(filt),
            meta={"backend": "mock_imu", "raw": float(raw)},
        )
