from __future__ import annotations
from abc import ABC, abstractmethod
from ...core.types import StimParams

class IStimBackend(ABC):
    @abstractmethod
    def apply(self, params: StimParams) -> None:
        ...
