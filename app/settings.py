"""Settings load only from env. No defaults that hide missing keys."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    base_url: str
    api_key: str
    evaluator_model: str


def load_settings() -> Settings:
    return Settings(
        base_url=os.environ.get("LLAMA_ROUTER_BASE_URL", "").rstrip("/"),
        api_key=os.environ.get("LLAMA_ROUTER_API_KEY", ""),
        evaluator_model=os.environ.get("EVALUATOR_MODEL", ""),
    )


def missing(settings: Settings) -> list[str]:
    out: list[str] = []
    if not settings.base_url:
        out.append("LLAMA_ROUTER_BASE_URL")
    if not settings.api_key:
        out.append("LLAMA_ROUTER_API_KEY")
    if not settings.evaluator_model:
        out.append("EVALUATOR_MODEL")
    return out
