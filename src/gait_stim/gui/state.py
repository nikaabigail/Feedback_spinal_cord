from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import numpy as np
from ..core.types import PoseFrame, StimParams

@dataclass
class GuiState:
    last_image: Optional[np.ndarray] = None
    last_pose: Optional[PoseFrame] = None
    last_stim: Optional[StimParams] = None
    psi_value: float = 0.0
