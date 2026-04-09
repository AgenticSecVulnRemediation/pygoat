import pytest

# Assumption: module path is importable as introduction.views
import introduction.views as views


def test_a9_lab_uses_yaml_safe_load(monkeypatch):
    # Arrange: ensure yaml.safe_load is invoked (and yaml.load is not)
    called = {"safe": 0, "load": 0}

    def fake_safe_load(stream):
        called["safe"] += 1
        return {"ok": True}

    def fake_load(*args, **kwargs):
        called["load"] += 1
        raise AssertionError("yaml.load should not be used")

    monkeypatch.setattr(views.yaml, "safe_load", fake_safe_load)
    monkeypatch.setattr(views.yaml, "load", fake_load)

    # Act: call the view function directly with a minimal request-like object
    class _Req:
        user = type("U", (), {"is_authenticated": True})()
        method = "POST"
        FILES = {"file": object()}

    # a9_lab wraps safe_load in try/except and returns a Django response; we only assert safe_load usage.
    views.a9_lab(_Req())

    # Assert
    assert called["safe"] == 1
    assert called["load"] == 0
