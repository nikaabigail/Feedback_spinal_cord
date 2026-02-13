from __future__ import annotations
from ...core.plugin import register_plugin
from ...core.config import Config
from ...core.types import PsiValue, KinematicsFrame, StimParams, StimChannelParams

@register_plugin("ctrl", "rule_based")
class RuleBasedController:
    """
    MVP - psi.value "толкает" амплитуду и выбор каналов.
    Логику потом усложню, на основе сырых даных; типы данных останутся.
    """
    def __init__(self, cfg: Config) -> None:
        self.n = int(cfg.get("controller", "stim_channels", default=4))
        self.amp_min = float(cfg.get("controller", "amp_min", default=0.0))
        self.amp_max = float(cfg.get("controller", "amp_max", default=5.0))

    def update(self, psi: PsiValue, kin: KinematicsFrame) -> StimParams:
        # psi в [-1..1] условно; clamp
        v = max(-1.0, min(1.0, float(psi.value)))
        # маппинг в амплитуду
        amp = self.amp_min + (abs(v) * (self.amp_max - self.amp_min))

        channels = []
        for i in range(self.n):
            # простая логика: если psi>0 — активируем половину каналов, если psi<0 — другую, по хорошему нужно будет доработать возможность выбора функкции
            # илидацию на стороне стимулятора, чтобы не было проблем с нечетным количеством каналов, сейчас просто делю на 2 и активирую либо первую, либо вторую половину
            # так же задаю частоту и длительность импульса, сейчас просто константные, но можно тоже маппить от psi/kinematics
            active_group = (i < self.n//2) if v >= 0 else (i >= self.n//2)
            ch = StimChannelParams(
                enabled=active_group,
                amplitude=amp if active_group else 0.0,
                frequency=50.0 if active_group else 0.0,
                burst_ms=200.0 if active_group else 0.0,
                phase_ms=0.0
            )
            channels.append(ch)

        return StimParams(ts=psi.ts, frame_id=psi.frame_id, channels=channels, meta={"psi": v})
