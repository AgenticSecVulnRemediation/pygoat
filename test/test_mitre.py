import pytest

# Assumption: module is importable as introduction.mitre
import introduction.mitre as mitre


def test_command_out_uses_shell_false(monkeypatch):
    # Arrange
    popen_calls = {}

    class DummyProc:
        def communicate(self):
            return (b"out", b"")

    def fake_popen(command, shell, stdout, stderr):
        popen_calls["command"] = command
        popen_calls["shell"] = shell
        return DummyProc()

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    # Act
    out, err = mitre.command_out(["nmap", "127.0.0.1"])

    # Assert
    assert out == b"out"
    assert err == b""
    assert popen_calls["shell"] is False


def test_mitre_lab_17_api_rejects_invalid_ip(monkeypatch):
    # Arrange
    class DummyRequest:
        method = "POST"

        def __init__(self, ip):
            self.POST = {"ip": ip}

    # Act
    resp = mitre.mitre_lab_17_api(DummyRequest("127.0.0.1; rm -rf /"))

    # Assert
    assert getattr(resp, "status_code", None) == 400
