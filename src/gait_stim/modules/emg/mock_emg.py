from __future__ import annotations
from ...core.plugin import register_plugin
from ...core.config import Config
import numpy as np

@register_plugin("emg", "mock_emg")
class MockEmg:
    def __init__(self, cfg: Config) -> None:
        self.n = 8

    def get_sample(self):
        return np.zeros((self.n,), dtype=np.float32)
