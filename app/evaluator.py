"""Evaluator: lightweight model picks the conversation model."""
from __future__ import annotations

import json

from .registry import Registry, resolve
from .router import chat
from .settings import Settings


def build_prompt(registry: Registry) -> str:
    names = ", ".join((registry.evaluator, *registry.conversations))
    return (
        "You are a router. Reply with JSON only: "
        '{"route": "<one of: ' + names + '>", '
        '"conversation": "<what to send that model>"}'
    )


def parse_reply(registry: Registry, text: str) -> tuple[str, str]:
    data = json.loads(text)
    route = resolve(registry, str(data["route"]))
    return route, str(data["conversation"])


def evaluate(settings: Settings, registry: Registry, user_text: str) -> tuple[str, str]:
    messages = [
        {"role": "system", "content": build_prompt(registry)},
        {"role": "user", "content": user_text},
    ]
    raw = chat(settings, registry.evaluator, messages)
    return parse_reply(registry, raw)
