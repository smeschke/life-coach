import pytest

from app import evaluator
from app.registry import Registry


def make_registry():
    return Registry(evaluator="eval-1", conversations=("planner", "checker"))


def test_parse_reply_ok():
    r = make_registry()
    route, convo = evaluator.parse_reply(r, '{"route": "planner", "conversation": "hi there"}')
    assert route == "planner"
    assert convo == "hi there"


def test_parse_reply_rejects_unknown():
    r = make_registry()
    with pytest.raises(KeyError):
        evaluator.parse_reply(r, '{"route": "nope", "conversation": "x"}')


def test_evaluate_calls_router(monkeypatch):
    from app.settings import Settings

    def fake_chat(settings, model, messages):
        assert model == "eval-1"
        return '{"route": "checker", "conversation": "check this"}'

    monkeypatch.setattr(evaluator, "chat", fake_chat)
    s = Settings(base_url="https://x", api_key="k", evaluator_model="eval-1")
    route, convo = evaluator.evaluate(s, make_registry(), "hello")
    assert (route, convo) == ("checker", "check this")
