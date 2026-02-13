from __future__ import annotations
from typing import Callable, Dict, Type, Any

_REGISTRY: Dict[str, Dict[str, Type[Any]]] = {}

def register_plugin(kind: str, name: str) -> Callable[[Type[Any]], Type[Any]]:
    def deco(cls: Type[Any]) -> Type[Any]:
        _REGISTRY.setdefault(kind, {})
        if name in _REGISTRY[kind]:
            raise ValueError(f"Плагин уже есть/зарегестрирован - {kind}:{name}")
        _REGISTRY[kind][name] = cls
        return cls
    return deco

def create(kind: str, name: str, **kwargs) -> Any:
    if kind not in _REGISTRY or name not in _REGISTRY[kind]:
        known = sorted(_REGISTRY.get(kind, {}).keys())
        raise KeyError(f"Неизвестный плагин - {kind}:{name}. Известные: {known}")
    return _REGISTRY[kind][name](**kwargs)

def known(kind: str) -> list[str]:
    return sorted(_REGISTRY.get(kind, {}).keys())
