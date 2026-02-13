from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

@dataclass(frozen=True)
class Config:
    raw: Dict[str, Any]

    @staticmethod
    def load(path: str | Path) -> "Config":
        p = Path(path)
        raw = json.loads(p.read_text(encoding="utf-8"))
        return Config(raw=raw)

    def get(self, *keys: str, default=None):
        cur: Any = self.raw
        for k in keys:
            if not isinstance(cur, dict) or k not in cur:
                return default
            cur = cur[k]
        return cur