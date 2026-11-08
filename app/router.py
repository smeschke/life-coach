"""Tiny OpenAI-compatible chat call for llama-router. No ladder, no fallback."""
from __future__ import annotations

import re

import requests

from .settings import Settings

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)


def strip_think(text: str) -> str:
    return _THINK_RE.sub("", text).strip()


def chat(settings: Settings, model: str, messages: list[dict], timeout: int = 60) -> str:
    url = f"{settings.base_url}/chat/completions"
    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {settings.api_key}"},
        json={"model": model, "messages": messages},
        timeout=timeout,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"router HTTP {resp.status_code}: {resp.text[:300]}")
    data = resp.json()
    text = data["choices"][0]["message"]["content"] or ""
    return strip_think(text)
