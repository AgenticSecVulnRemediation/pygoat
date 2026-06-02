import datetime
from types import SimpleNamespace

import pytest

# Assumption: module import path is introduction.mitre
from introduction import mitre


def _fake_request(ip: str):
    return SimpleNamespace(method="POST", POST={"ip": ip})


def test_mitre_lab_17_api_invalid_ip_returns_400(monkeypatch):
    """Command injection hardening: reject non-IP input before invoking nmap."""
    # Arrange: ensure command_out is NOT called on invalid ip
    def _boom(_cmd):  # pragma: no cover
        raise AssertionError("command_out should not be called for invalid IP")

    monkeypatch.setattr(mitre, "command_out", _boom)

    # Act
    resp = mitre.mitre_lab_17_api(_fake_request("127.0.0.1; whoami"))

    # Assert
    assert getattr(resp, "status_code", None) == 400


def test_command_out_does_not_use_shell_true(monkeypatch):
    """Regression: command_out must call subprocess with shell=False."""
    captured = {}

    class _FakePopen:
        def __init__(self, cmd, shell, stdout, stderr):
            captured["cmd"] = cmd
            captured["shell"] = shell

        def communicate(self):
            return (b"", b"")

    monkeypatch.setattr(mitre.subprocess, "Popen", _FakePopen)

    # Act
    mitre.command_out(["nmap", "127.0.0.1"])

    # Assert
    assert captured["shell"] is False
