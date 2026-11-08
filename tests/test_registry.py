import pytest

from app.registry import load_registry, resolve


def test_load_registry_splits_names(monkeypatch):
    monkeypatch.setenv("CONVERSATION_MODELS", "planner, checker")
    r = load_registry("eval-1")
    assert r.evaluator == "eval-1"
    assert r.conversations == ("planner", "checker")


def test_resolve_accepts_wanted(monkeypatch):
    monkeypatch.setenv("CONVERSATION_MODELS", "planner")
    r = load_registry("eval-1")
    assert resolve(r, "planner") == "planner"


def test_resolve_rejects_unknown(monkeypatch):
    monkeypatch.setenv("CONVERSATION_MODELS", "planner")
    r = load_registry("eval-1")
    with pytest.raises(KeyError):
        resolve(r, "nope")
