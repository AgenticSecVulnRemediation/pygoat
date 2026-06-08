import pytest


# Assumption: module path is introduction.views as indicated by file_path.
from introduction.views import a9_lab


def test_a9_lab_uses_safe_load(monkeypatch):
    """Regression: YAML parsing must use safe_load (not yaml.load) to prevent unsafe deserialization."""

    import introduction.views as views

    called = {"safe": False, "load": False}

    def fake_safe_load(file_obj):
        called["safe"] = True
        return {"ok": True}

    def fake_load(*args, **kwargs):
        called["load"] = True
        raise AssertionError("yaml.load must not be used")

    # Patch yaml functions
    monkeypatch.setattr(views.yaml, "safe_load", fake_safe_load)
    monkeypatch.setattr(views.yaml, "load", fake_load)

    # Patch render to return data for assertion
    monkeypatch.setattr(views, "render", lambda request, template, context=None: context)

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        user = DummyUser()
        method = "POST"
        FILES = {"file": object()}

    ctx = a9_lab(DummyRequest())
    assert called["safe"] is True
    assert called["load"] is False
    assert ctx["data"] == {"ok": True}
