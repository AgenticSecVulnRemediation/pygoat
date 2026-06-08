import json

import pytest

# Assumption: Django view lives at introduction.mitre
from introduction import mitre


def test_mitre_lab_17_api_rejects_invalid_ip_returns_400(rf):
    """Fix adds explicit IPv4 format validation; invalid input must be rejected."""
    request = rf.post("/mitre/17/api", data={"ip": "127.0.0.1; rm -rf /"})

    response = mitre.mitre_lab_17_api(request)

    assert response.status_code == 400
    assert b"Invalid IP address" in response.content


def test_mitre_lab_17_api_uses_subprocess_without_shell(rf, monkeypatch):
    """Fix changes subprocess invocation to shell=False with argv list."""

    called = {}

    def fake_popen(cmd, shell, stdout, stderr):
        called["cmd"] = cmd
        called["shell"] = shell

        class Proc:
            def communicate(self_inner):
                # minimal output that matches parsing logic: needs "STATE SERVICE\n\n" then at least one port line.
                return (
                    b"Some header\nSTATE SERVICE\n\n22/tcp open ssh\n",
                    b"",
                )

        return Proc()

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    request = rf.post("/mitre/17/api", data={"ip": "127.0.0.1"})
    response = mitre.mitre_lab_17_api(request)

    assert response.status_code == 200
    payload = json.loads(response.content.decode("utf-8"))
    assert "ports" in payload

    assert called["shell"] is False
    assert called["cmd"] == ["nmap", "127.0.0.1"]
