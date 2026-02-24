# src/gait_stim/core/bootstrap.py
"""
Импортирует все модули с @register_plugin, чтобы заполнить реестр плагинов.
"""
from importlib import import_module

_MODULES = [
    # video
    "gait_stim.modules.video.opencv_source",
    # Две камеры
    "gait_stim.modules.video.opencv_dual_source",
    # pose
    "gait_stim.modules.pose.yolo_stub",
    "gait_stim.modules.pose.dlc_stub",
    # kinematics
    "gait_stim.modules.kinematics.simple_kin",
    # psi
    "gait_stim.modules.asymmetry.manual_psi",
    # controller
    "gait_stim.modules.controller.rule_based",
    # stim
    "gait_stim.modules.stim.mock_stim",
    # emg (пока не используется в пайплайне, но пусть регистрируется)
    "gait_stim.modules.emg.mock_emg",
]

def bootstrap_plugins() -> None:
    for m in _MODULES:
        import_module(m)
