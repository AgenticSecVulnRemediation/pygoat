import pytest

# Assumption: module path is importable as introduction.mitre in test environment.
from introduction import mitre


def test_mitre_lab_17_api_rejects_invalid_ip_and_does_not_invoke_subprocess(monkeypatch):
    # Arrange
    class DummyRequest:
        method = "POST"
        POST = {"ip": "127.0.0.1; rm -rf /"}

    popen_called = {"called": False}

    def fake_popen(*args, **kwargs):
        popen_called["called"] = True
        raise AssertionError("subprocess.Popen should not be called for invalid IP")

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    # Act
    resp = mitre.mitre_lab_17_api(DummyRequest())

    # Assert
    assert resp.status_code == 400
    assert b"Invalid IP address" in resp.content
    assert popen_called["called"] is False


def test_command_out_uses_shell_false(monkeypatch):
    # Arrange
    captured = {"kwargs": None}

    class FakeProcess:
        def communicate(self):
            return b"", b""

    def fake_popen(*args, **kwargs):
        captured["kwargs"] = kwargs
        return FakeProcess()

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    # Act
    mitre.command_out(["nmap", "127.0.0.1"])

    # Assert
    assert captured["kwargs"].get("shell") is False
