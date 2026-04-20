import types
from unittest.mock import MagicMock

import pytest

# Assumption: Django app module path is "introduction" and mitre_lab_17_api is importable from introduction.mitre
from introduction.mitre import mitre_lab_17_api


def _make_request(ip: str):
    req = types.SimpleNamespace()
    req.method = "POST"
    req.POST = {"ip": ip}
    return req


def test_mitre_lab_17_api_rejects_invalid_ip_returns_400(monkeypatch):
    # Arrange
    request = _make_request("127.0.0.1; whoami")

    popen_spy = MagicMock()
    monkeypatch.setattr("introduction.mitre.subprocess.Popen", popen_spy)

    # Act
    response = mitre_lab_17_api(request)

    # Assert
    assert response.status_code == 400
    # Ensure no subprocess execution for invalid input
    popen_spy.assert_not_called()


def test_mitre_lab_17_api_executes_nmap_without_shell_and_uses_argv_list(monkeypatch):
    # Arrange
    request = _make_request("127.0.0.1")

    process = MagicMock()
    process.communicate.return_value = (b"STATE SERVICE\n\n22/tcp open ssh\n", b"")

    def _popen(args, **kwargs):
        # Assert (within call) - critical security properties
        assert args == ["nmap", "127.0.0.1"]
        assert kwargs.get("shell") is False
        return process

    monkeypatch.setattr("introduction.mitre.subprocess.Popen", _popen)

    # Act
    response = mitre_lab_17_api(request)

    # Assert
    assert response.status_code == 200
