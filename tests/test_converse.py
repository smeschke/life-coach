from app import converse
from app.registry import Registry
from app.settings import Settings


def test_run_conversation_uses_route(monkeypatch):
    seen = {}

    def fake_chat(settings, model, messages):
        seen["model"] = model
        seen["text"] = messages[0]["content"]
        return "reply-text"

    monkeypatch.setattr(converse, "chat", fake_chat)
    s = Settings(base_url="https://x", api_key="k", evaluator_model="eval-1")
    r = Registry(evaluator="eval-1", conversations=("planner",))
    out = converse.run_conversation(s, r, "planner", "hello planner")
    assert out == "reply-text"
    assert seen == {"model": "planner", "text": "hello planner"}
