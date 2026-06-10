import subprocess

import pytest

import introduction.mitre as mitre


def test_mitre_lab_17_api_rejects_invalid_ip_without_running_nmap(monkeypatch):
    """Regression test for command injection hardening:
    - invalid IP should return HTTP 400
    - subprocess should never be invoked
    """

    class DummyRequest:
        method = "POST"
        POST = {"ip": "127.0.0.1; cat /etc/passwd"}

    def popen_should_not_be_called(*args, **kwargs):
        raise AssertionError("subprocess.Popen should not be called for invalid IP")

    monkeypatch.setattr(subprocess, "Popen", popen_should_not_be_called)

    resp = mitre.mitre_lab_17_api(DummyRequest())

    assert resp.status_code == 400


def test_mitre_lab_17_api_uses_list_args_shell_false_behavior(monkeypatch):
    """Ensure command is invoked without shell string concatenation.

    We assert that subprocess is called with a list (['nmap', ip]) and no shell=True.
    """

    class DummyRequest:
        method = "POST"
        POST = {"ip": "127.0.0.1"}

    calls = {}

    class DummyPopen:
        def __init__(self, args, stdout=None, stderr=None, **kwargs):
            calls["args"] = args
            calls["kwargs"] = kwargs

        def communicate(self):
            # Minimal nmap-like output matching code's regex
            out = b"STATE SERVICE\n\n80/tcp open http\n"
            err = b""
            return out, err

    monkeypatch.setattr(subprocess, "Popen", DummyPopen)

    resp = mitre.mitre_lab_17_api(DummyRequest())

    assert resp.status_code == 200
    assert calls["args"] == ["nmap", "127.0.0.1"]
    assert calls["kwargs"].get("shell") is None
