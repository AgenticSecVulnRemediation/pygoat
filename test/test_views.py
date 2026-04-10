import importlib

import pytest


def test_cmd_lab_rejects_invalid_domain_before_subprocess(monkeypatch):
    # Arrange
    views = importlib.import_module('introduction.views')

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        user = DummyUser()
        method = "POST"
        POST = {"domain": "example.com;rm -rf /", "os": "linux"}

    def fake_popen(*args, **kwargs):
        raise AssertionError("subprocess.Popen should not be called for invalid domain")

    monkeypatch.setattr(views.subprocess, "Popen", fake_popen)

    # Act / Assert
    with pytest.raises(ValueError):
        views.cmd_lab(DummyRequest())
