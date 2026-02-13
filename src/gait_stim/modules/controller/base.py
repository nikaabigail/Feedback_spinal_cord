from __future__ import annotations
from abc import ABC, abstractmethod
from ...core.types import PsiValue, KinematicsFrame, StimParams

class IController(ABC):
    @abstractmethod
    def update(self, psi: PsiValue, kin: KinematicsFrame) -> StimParams:
        ...