from __future__ import annotations
from abc import ABC, abstractmethod

class IEmgSource(ABC):
    @abstractmethod
    def get_sample(self):
        ...
