import os

from app.settings import load_settings, missing


def test_load_settings_reads_env(monkeypatch):
    monkeypatch.setenv("LLAMA_ROUTER_BASE_URL", "https://x.example/v1/")
    monkeypatch.setenv("LLAMA_ROUTER_API_KEY", "k")
    monkeypatch.setenv("EVALUATOR_MODEL", "eval-1")
    s = load_settings()
    assert s.base_url == "https://x.example/v1"
    assert s.api_key == "k"
    assert s.evaluator_model == "eval-1"
    assert missing(s) == []


def test_missing_lists_blanks(monkeypatch):
    monkeypatch.delenv("LLAMA_ROUTER_BASE_URL", raising=False)
    monkeypatch.delenv("LLAMA_ROUTER_API_KEY", raising=False)
    monkeypatch.delenv("EVALUATOR_MODEL", raising=False)
    s = load_settings()
    assert "LLAMA_ROUTER_BASE_URL" in missing(s)


def test_chat_returns_content(monkeypatch):
    from app import router
    from app.settings import Settings

    class FakeResp:
        status_code = 200
        text = "ok"

        def json(self):
            return {"choices": [{"message": {"content": "<think>h</think>hi"}}]}

    monkeypatch.setattr(router.requests, "post", lambda *a, **k: FakeResp())
    s = Settings(base_url="https://x", api_key="k", evaluator_model="e")
    assert router.chat(s, "e", [{"role": "user", "content": "hi"}]) == "hi"
