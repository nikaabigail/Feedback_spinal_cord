from __future__ import annotations
from abc import ABC, abstractmethod
from ...core.types import KinematicsFrame, PsiValue

class IPsi(ABC):
    @abstractmethod
    def compute(self, kin: KinematicsFrame) -> PsiValue:
        ...