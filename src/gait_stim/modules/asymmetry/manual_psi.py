from __future__ import annotations
from ...core.plugin import register_plugin
from ...core.config import Config
from ...core.bus import Bus, Message
from ...core.types import KinematicsFrame, PsiValue

@register_plugin("psi", "manual_psi")
class ManualPsi:
    """
    Оптяь же заглушка, сейча Ψ задается вручную (GUI slider).
    Потом заменю на алгоритмический модуль, интерфейс тот же.
    """
    def __init__(self, cfg: Config, bus: Bus) -> None:
        self.value = float(cfg.get("psi", "initial_value", default=0.0))
        bus.subscribe("gui.psi", self._on_gui_psi)

    def _on_gui_psi(self, msg: Message) -> None:
        try:
            self.value = float(msg.payload)
        except Exception:
            pass

    def compute(self, kin: KinematicsFrame) -> PsiValue:
        return PsiValue(ts=kin.ts, frame_id=kin.frame_id, value=self.value, meta={"source": "manual"})
