"""CLI loop: evaluate then run. One turn is testable without stdin."""
from __future__ import annotations

from . import converse, evaluator
from .registry import Registry, load_registry
from .settings import Settings, load_settings, missing


def chat_once(settings: Settings, registry: Registry, user_text: str) -> tuple[str, str, str]:
    route, conversation = evaluator.evaluate(settings, registry, user_text)
    reply = converse.run_conversation(settings, registry, route, conversation)
    return route, conversation, reply


def main() -> int:
    settings = load_settings()
    gaps = missing(settings)
    if gaps:
        print("Missing in .env: " + ", ".join(gaps))
        return 1
    registry = load_registry(settings.evaluator_model)
    print("life-coach ready. Type quit to exit.")
    while True:
        try:
            user_text = input("> ").strip()
        except EOFError:
            break
        if user_text.lower() in ("quit", "exit"):
            break
        if not user_text:
            continue
        route, _, reply = chat_once(settings, registry, user_text)
        print(f"[{route}] {reply}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
