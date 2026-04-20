import types
from unittest.mock import MagicMock

import pytest

# Assumption: Django app module path is "introduction" and a9_lab is importable from introduction.views
from introduction.views import a9_lab


def _make_request(file_obj):
    req = types.SimpleNamespace()
    req.user = types.SimpleNamespace(is_authenticated=True)
    req.method = "POST"
    req.FILES = {"file": file_obj}
    return req


def test_a9_lab_uses_yaml_safe_load(monkeypatch):
    # Arrange
    request = _make_request(file_obj=object())

    safe_load_spy = MagicMock(return_value={"k": "v"})
    load_spy = MagicMock(side_effect=AssertionError("yaml.load should not be used"))

    monkeypatch.setattr("introduction.views.yaml.safe_load", safe_load_spy)
    monkeypatch.setattr("introduction.views.yaml.load", load_spy)

    render_spy = MagicMock(return_value="rendered")
    monkeypatch.setattr("introduction.views.render", render_spy)

    # Act
    result = a9_lab(request)

    # Assert
    assert result == "rendered"
    safe_load_spy.assert_called_once()
    load_spy.assert_not_called()
