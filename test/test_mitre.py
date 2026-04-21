import os
import types

import pytest

# Assumption: module path is importable as introduction.mitre
from introduction import mitre


def _make_request(ip_value):
    req = types.SimpleNamespace()
    req.method = "POST"
    req.POST = {"ip": ip_value}
    req.COOKIES = {}
    return req


def test_mitre_lab_17_api_rejects_invalid_ip_returns_400(monkeypatch):
    # Arrange
    req = _make_request("127.0.0.1; rm -rf /")
    monkeypatch.setattr(mitre, "command_out", lambda cmd: (b"", b""))

    # Act
    resp = mitre.mitre_lab_17_api(req)

    # Assert
    assert getattr(resp, "status_code", None) == 400


def test_mitre_lab_17_api_uses_list_command_and_shell_false(monkeypatch):
    # Arrange
    seen = {}

    def fake_popen(cmd, shell, stdout, stderr):
        seen["cmd"] = cmd
        seen["shell"] = shell

        class P:
            def communicate(self):
                # minimal output to satisfy regex in handler
                return (b"STATE SERVICE\n\n80/tcp open http\n", b"")

        return P()

    req = _make_request("127.0.0.1")
    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    # Act
    resp = mitre.mitre_lab_17_api(req)

    # Assert
    assert seen["cmd"] == ["nmap", "127.0.0.1"]
    assert seen["shell"] is False
    assert resp.status_code == 200
