from __future__ import annotations
from abc import ABC, abstractmethod
from ...core.types import PoseFrame, KinematicsFrame

class IKinematics(ABC):
    @abstractmethod
    def compute(self, pose: PoseFrame) -> KinematicsFrame:
        ...
