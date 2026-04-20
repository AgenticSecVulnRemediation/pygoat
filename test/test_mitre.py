import types

import pytest


def test_mitre_lab_17_api_rejects_non_ip_and_does_not_execute(monkeypatch):
    """Delta test: mitre_lab_17_api now validates IP and uses Popen(shell=False).

    Ensure invalid IP returns 400 and command_out is not invoked.
    """

    import introduction.mitre as mitre

    command_out_called = {"count": 0}

    def fake_command_out(command):
        command_out_called["count"] += 1
        return (b"", b"")

    monkeypatch.setattr(mitre, "command_out", fake_command_out)

    class DummyRequest:
        method = "POST"

        def __init__(self, ip):
            self.POST = {"ip": ip}

    resp = mitre.mitre_lab_17_api(DummyRequest("8.8.8.8; rm -rf /"))

    assert resp.status_code == 400
    assert command_out_called["count"] == 0


def test_command_out_uses_shell_false(monkeypatch):
    """Delta test: command_out now uses subprocess.Popen(shell=False)."""

    import introduction.mitre as mitre

    popen_args = {}

    class DummyProc:
        def communicate(self):
            return (b"out", b"err")

    def fake_popen(cmd, shell, stdout, stderr):
        popen_args["shell"] = shell
        popen_args["cmd"] = cmd
        return DummyProc()

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    out, err = mitre.command_out(["nmap", "127.0.0.1"])

    assert out == b"out"
    assert err == b"err"
    assert popen_args["shell"] is False
