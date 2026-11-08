from app import cli
from app.registry import Registry
from app.settings import Settings


def test_chat_once_wires_evaluator_to_runner(monkeypatch):
    from app import converse, evaluator

    monkeypatch.setattr(
        evaluator, "evaluate", lambda *a, **k: ("planner", "plan this")
    )
    monkeypatch.setattr(
        converse, "run_conversation", lambda *a, **k: "done"
    )
    s = Settings(base_url="https://x", api_key="k", evaluator_model="eval-1")
    r = Registry(evaluator="eval-1", conversations=("planner",))
    assert cli.chat_once(s, r, "hi") == ("planner", "plan this", "done")
