from __future__ import annotations
from abc import ABC, abstractmethod
from ...core.types import VideoFrame, PoseFrame

class IPoseEstimator(ABC):
    @abstractmethod
    def infer(self, frame: VideoFrame) -> PoseFrame:
        ...