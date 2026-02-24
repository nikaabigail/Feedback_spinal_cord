from __future__ import annotations
from typing import Optional
import time

from .bus import Bus
from .config import Config
from .plugin import create
from .types import VideoFrame, PoseFrame, KinematicsFrame, PsiValue, StimParams
from .bootstrap import bootstrap_plugins

class Pipeline:
    def __init__(self, cfg: Config, bus: Optional[Bus] = None) -> None:
        bootstrap_plugins()
        self.cfg = cfg
        self.bus = bus or Bus()

        self.video = create("video", cfg.get("video", "source"), cfg=cfg)
        self.pose  = create("pose",  cfg.get("pose", "backend"), cfg=cfg)
        self.kin   = create("kin",   "simple_kin", cfg=cfg)
        self.psi   = create("psi",   cfg.get("psi", "backend"), cfg=cfg, bus=self.bus)
        self.ctrl  = create("ctrl",  cfg.get("controller", "backend"), cfg=cfg)
        self.stim  = create("stim",  cfg.get("stim", "backend"), cfg=cfg, bus=self.bus)

        self._running = False

    def step(self) -> None:
        frames = self.video.get_frames()  # dict: {"control": VideoFrame, "experimental": VideoFrame}

        # публикуем оба видео
        for name, vf in frames.items():
            self.bus.publish(f"video.frame.{name}", vf)

        # поза на обоих потоках (пока одинаково; позже можно разный backend)
        poses = {}
        for name, vf in frames.items():
            pf = self.pose.infer(vf)
            poses[name] = pf
            self.bus.publish(f"pose.frame.{name}", pf)

        # MVP: дальше берем experimental как “рабочий” поток (так проще)
        pf_exp = poses.get("experimental") or next(iter(poses.values()))
        kf = self.kin.compute(pf_exp)
        self.bus.publish("kin.frame", kf)

        ps = self.psi.compute(kf)
        self.bus.publish("psi.value", ps)

        sp = self.ctrl.update(ps, kf)
        self.bus.publish("stim.params", sp)
        self.stim.apply(sp)

    def run_forever(self) -> None:
        self._running = True
        while self._running:
            self.step()

    def stop(self) -> None:
        self._running = False