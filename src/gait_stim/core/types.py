from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

Timestamp = float

@dataclass(frozen=True)
class VideoFrame:
    ts: Timestamp
    frame_id: int
    image: np.ndarray
    camera_id: int = 0
    camera_name: str = "cam0"

@dataclass(frozen=True)
class PoseFrame:
    ts: Timestamp
    frame_id: int
    keypoints_xy: np.ndarray # Размер (K, 2)
    keypoints_conf: np.ndarray # (K,)
    meta: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class KinematicsFrame:
    ts: Timestamp
    frame_id: int
    features: Dict[str, float] # угол, длительность
    events: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class PsiValue:
    ts: Timestamp
    frame_id: int
    value: float
    meta: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class StimChannelParams:
    enabled: bool = True
    amplitude: float = 0.0
    frequency: float = 0.0
    burst_ms: float = 0.0
    phase_ms: float = 0.0

@dataclass(frozen=True)
class StimParams:
    ts: Timestamp
    frame_id: int
    channels: List[StimChannelParams]
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ImuSample:
    ts: Timestamp
    frame_id: int
    source: str
    value: float
    meta: Dict[str, Any] = field(default_factory=dict)
