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


def test_cmd_lab_rejects_domain_with_shell_metacharacters_before_subprocess(monkeypatch):
    # Arrange - the new code raises ValueError for invalid domains
    request = _make_request("example.com;whoami", os_name="linux")

    popen_spy = MagicMock()
    monkeypatch.setattr("introduction.views.subprocess.Popen", popen_spy)

    # Act / Assert
    with pytest.raises(ValueError):
        cmd_lab(request)
    popen_spy.assert_not_called()


def test_cmd_lab_uses_shell_false_and_list_args(monkeypatch):
    # Arrange
    request = _make_request("example.com", os_name="win")

    proc = MagicMock()
    proc.communicate.return_value = (b"out", b"")

    popen_spy = MagicMock(return_value=proc)
    monkeypatch.setattr("introduction.views.subprocess.Popen", popen_spy)

    # Also patch render to avoid template dependency
    render_spy = MagicMock(return_value="rendered")
    monkeypatch.setattr("introduction.views.render", render_spy)

    # Act
    result = cmd_lab(request)

    # Assert
    assert result == "rendered"
    args, kwargs = popen_spy.call_args
    assert args[0] == ["nslookup", "example.com"]
    assert kwargs.get("shell") is False
