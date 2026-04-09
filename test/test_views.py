import io

import pytest

# Assumption: Django app module path is introduction.views
import introduction.views as views


def test_a9_lab_uses_yaml_safe_load(monkeypatch):
    # Arrange: ensure yaml.safe_load is used and yaml.load is not.
    called = {"safe": False}

    def fake_safe_load(file_obj):
        called["safe"] = True
        return {"ok": True}

    def fake_load(*args, **kwargs):
        raise AssertionError("yaml.load should not be called")

    monkeypatch.setattr(views.yaml, "safe_load", fake_safe_load)
    monkeypatch.setattr(views.yaml, "load", fake_load)

    # Act
    result = views.yaml.safe_load(io.StringIO("a: 1"))

    # Assert
    assert called["safe"] is True
    assert result == {"ok": True}
