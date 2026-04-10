import re

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
    assert b"Invalid IP format" in resp.content
    assert popen_called["called"] is False


def test_mitre_lab_17_api_uses_argv_without_shell(monkeypatch):
    # Arrange
    class DummyRequest:
        method = "POST"
        POST = {"ip": "127.0.0.1"}

    captured = {"args": None, "kwargs": None}

    class FakeProcess:
        def communicate(self):
            # Minimal output to satisfy regex parsing in view
            stdout = b"STATE SERVICE\n\n80/tcp open http\n"
            stderr = b""
            return stdout, stderr

    def fake_popen(args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs
        return FakeProcess()

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    # Act
    resp = mitre.mitre_lab_17_api(DummyRequest())

    # Assert
    assert resp.status_code == 200
    assert captured["args"] == ["nmap", "127.0.0.1"]
    assert captured["kwargs"].get("shell") is None
    assert captured["kwargs"]["stdout"] is not None
    assert captured["kwargs"]["stderr"] is not None
