"""Conversation runner: send the string to the routed model."""
from __future__ import annotations

from .registry import Registry, resolve
from .router import chat
from .settings import Settings


def run_conversation(settings: Settings, registry: Registry, route: str, conversation: str) -> str:
    model = resolve(registry, route)
    return chat(settings, model, [{"role": "user", "content": conversation}])
