import types
from unittest.mock import MagicMock

import pytest

# Assumption: Django app module path is "introduction" and cmd_lab is importable from introduction.views
from introduction.views import cmd_lab


def _make_request(domain: str, os_name: str = "linux"):
    req = types.SimpleNamespace()
    req.method = "POST"
    req.user = types.SimpleNamespace(is_authenticated=True)
    req.POST = {"domain": domain, "os": os_name}
    return req


def test_cmd_lab_uses_subprocess_without_shell_and_list_args(monkeypatch):
    # Arrange
    request = _make_request("example.com", os_name="linux")

    proc = MagicMock()
    proc.communicate.return_value = (b"out", b"")

    popen_spy = MagicMock(return_value=proc)
    monkeypatch.setattr("introduction.views.subprocess.Popen", popen_spy)

    # Act
    response = cmd_lab(request)

    # Assert
    popen_spy.assert_called_once()
    args, kwargs = popen_spy.call_args
    assert args[0] == ["dig", "example.com"]
    assert kwargs.get("shell") is None or kwargs.get("shell") is False
