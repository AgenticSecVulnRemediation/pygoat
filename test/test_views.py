import io

import pytest
import yaml


def test_views_a9_lab_uses_yaml_safe_load(monkeypatch):
    # Arrange
    # We assert the application code calls yaml.safe_load (changed behavior).
    import introduction.views as views

    safe_load_called = {"count": 0}

    def fake_safe_load(_stream):
        safe_load_called["count"] += 1
        # Return something renderable
        return {"ok": True}

    monkeypatch.setattr(views.yaml, "safe_load", fake_safe_load)

    # Avoid Django template rendering dependency; just return context.
    def fake_render(_request, _template, context=None, **_kwargs):
        return context or {}

    monkeypatch.setattr(views, "render", fake_render)

    class _DummyUser:
        is_authenticated = True

    class _DummyRequest:
        method = "POST"
        user = _DummyUser()
        FILES = {"file": io.BytesIO(b"a: 1\n")}

    # Act
    context = views.a9_lab(_DummyRequest())

    # Assert
    assert safe_load_called["count"] == 1
    assert context.get("data") == {"ok": True}
