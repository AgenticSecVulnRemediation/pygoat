import pytest

import introduction.views as views


def test_a9_lab_uses_safe_yaml_load(monkeypatch):
    """Regression test: ensure yaml.load is NOT used, and yaml.safe_load is used."""

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        user = DummyUser()
        method = "POST"
        FILES = {"file": object()}

    # If yaml.load gets called, fail.
    def load_should_not_be_called(*args, **kwargs):
        raise AssertionError("yaml.load should not be used")

    monkeypatch.setattr(views.yaml, "load", load_should_not_be_called)

    captured = {}

    def safe_load(file_obj):
        captured["called"] = True
        return {"k": "v"}

    monkeypatch.setattr(views.yaml, "safe_load", safe_load)

    # Patch render to just return the context for assertion
    def fake_render(request, template, context=None, **kwargs):
        return context

    monkeypatch.setattr(views, "render", fake_render)

    result = views.a9_lab(DummyRequest())

    assert captured.get("called") is True
    assert result["data"] == {"k": "v"}
