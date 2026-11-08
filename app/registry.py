"""Wanted models. Coach names them. Backend must provide them."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Registry:
    evaluator: str
    conversations: tuple[str, ...]


def load_registry(evaluator_model: str) -> Registry:
    raw = os.environ.get("CONVERSATION_MODELS", "")
    names = tuple(n.strip() for n in raw.split(",") if n.strip())
    return Registry(evaluator=evaluator_model, conversations=names)


def resolve(registry: Registry, route: str) -> str:
    if route == registry.evaluator:
        return route
    if route in registry.conversations:
        return route
    want = ", ".join((registry.evaluator, *registry.conversations)) or "(none)"
    raise KeyError(f"unknown model {route!r}. Wanted: {want}")
