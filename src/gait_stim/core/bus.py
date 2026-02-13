from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Dict, List

@dataclass
class Message:
    topic: str
    payload: Any

class Bus:
    def __init__(self) -> None:
        self._subs: Dict[str, List[Callable[[Message], None]]] = {}

    def subscribe(self, topic: str, fn: Callable[[Message], None]) -> None:
        self._subs.setdefault(topic, []).append(fn)

    def publish(self, topic: str, payload: Any) -> None:
        msg = Message(topic=topic, payload=payload)
        for fn in self._subs.get(topic, []):
            fn(msg)