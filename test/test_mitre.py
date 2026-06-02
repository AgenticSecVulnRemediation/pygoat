# Assumptions:
# - The project uses pytest.
# - The Django view functions in introduction.mitre can be tested as plain callables by providing a request-like object.
# - We avoid importing Django's HttpRequest; instead, we use a lightweight stub with a POST dict.

import subprocess

import pytest

from introduction import mitre


class _RequestStub:
    def __init__(self, method="POST", post=None):
        self.method = method
        self.POST = post or {}


def test_mitre_lab_17_api_rejects_non_ip_and_does_not_execute_command(monkeypatch):
    """Regression test for command-injection fix:

    - Previously, ip was concatenated into a shell=True command string.
    - Now, invalid IPs should be rejected and subprocess should not be invoked.
    """

    called = {"count": 0}

    def _boom(*args, **kwargs):
        called["count"] += 1
        raise AssertionError("command_out/subprocess should not be called for invalid ip")

    monkeypatch.setattr(mitre, "command_out", _boom)

    req = _RequestStub(post={"ip": "127.0.0.1; whoami"})
    resp = mitre.mitre_lab_17_api(req)

    assert getattr(resp, "status_code", None) == 400
    assert "Invalid IP" in resp.content.decode("utf-8")
    assert called["count"] == 0


def test_command_out_invokes_popen_with_shell_false(monkeypatch):
    """Ensures command_out does not use a shell."""

    captured = {}

    class _FakeProc:
        def communicate(self):
            return (b"ok", b"")

    def _fake_popen(cmd, shell, stdout, stderr):
        captured["cmd"] = cmd
        captured["shell"] = shell
        return _FakeProc()

    monkeypatch.setattr(subprocess, "Popen", _fake_popen)

    out, err = mitre.command_out(["nmap", "127.0.0.1"])

    assert out == b"ok"
    assert err == b""
    assert captured["cmd"] == ["nmap", "127.0.0.1"]
    assert captured["shell"] is False
