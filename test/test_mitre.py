import json

import pytest


def test_command_out_uses_shell_false(monkeypatch):
    """Delta behavior: subprocess.Popen called with shell=False."""

    import introduction.mitre as mitre

    captured = {}

    class FakeProc:
        def communicate(self):
            return (b"out", b"err")

    def fake_popen(cmd, shell, stdout, stderr):
        captured["cmd"] = cmd
        captured["shell"] = shell
        return FakeProc()

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    out, err = mitre.command_out(["echo", "hi"])

    assert captured["cmd"] == ["echo", "hi"]
    assert captured["shell"] is False
    assert out == b"out"
    assert err == b"err"


def test_mitre_lab_17_api_builds_command_as_list(monkeypatch):
    """Delta behavior: nmap command built as ['nmap', ip] instead of shell string."""

    import introduction.mitre as mitre

    # Stub out command_out to capture the command passed
    captured = {}

    def fake_command_out(command):
        captured["command"] = command
        # minimal nmap-like output matching parsing regex
        res = (
            "Starting Nmap\n"
            "STATE SERVICE\n\n"
            "80/tcp open http\n"
            "\n"
        ).encode()
        return res, b""

    monkeypatch.setattr(mitre, "command_out", fake_command_out)

    # Replace JsonResponse with a simple dict to avoid needing Django test framework
    monkeypatch.setattr(mitre, "JsonResponse", lambda payload: payload)

    class Request:
        method = "POST"

        def __init__(self):
            self.POST = {"ip": "127.0.0.1"}

    resp = mitre.mitre_lab_17_api(Request())

    assert captured["command"] == ["nmap", "127.0.0.1"]
    assert "ports" in resp
    assert resp["ports"] == ["80/tcp open http"]
