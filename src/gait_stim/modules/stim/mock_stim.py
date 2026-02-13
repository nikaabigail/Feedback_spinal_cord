from __future__ import annotations
from ...core.plugin import register_plugin
from ...core.config import Config
from ...core.bus import Bus, Message
from ...core.types import StimParams

@register_plugin("stim", "mock_stim")
class MockStim:
    """
    Заглушка, ничего не стимулирует, только публикует в bus и может логировать.
    """
    def __init__(self, cfg: Config, bus: Bus) -> None:
        self.bus = bus

    def apply(self, params: StimParams) -> None:
        # можно лог, можно в GUI, пока просто в bus
        self.bus.publish("stim.applied", params)
