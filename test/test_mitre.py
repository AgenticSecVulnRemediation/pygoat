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


def test_mitre_lab_17_api_rejects_invalid_ip_format_and_does_not_run_subprocess(monkeypatch):
    # Arrange
    request = _make_request("127.0.0.1;whoami")

    popen_spy = MagicMock()
    monkeypatch.setattr("introduction.mitre.subprocess.Popen", popen_spy)

    # Act
    response = mitre_lab_17_api(request)

    # Assert
    assert response.status_code == 400
    popen_spy.assert_not_called()


def test_mitre_lab_17_api_uses_argv_list_for_nmap(monkeypatch):
    # Arrange
    request = _make_request("127.0.0.1")

    process = MagicMock()
    process.communicate.return_value = (b"STATE SERVICE\n\n22/tcp open ssh\n", b"")

    def _popen(args, **kwargs):
        assert args == ["nmap", "127.0.0.1"]
        # In this variant, shell kwarg isn't passed (default False)
        assert "shell" not in kwargs
        return process

    monkeypatch.setattr("introduction.mitre.subprocess.Popen", _popen)

    # Act
    response = mitre_lab_17_api(request)

    # Assert
    assert response.status_code == 200
