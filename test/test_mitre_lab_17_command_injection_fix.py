import types

import pytest


@pytest.mark.parametrize(
    "ip",
    [
        "127.0.0.1; echo pwned",
        "127.0.0.1 && whoami",
        "1.2.3.4 | cat /etc/passwd",
        "not-an-ip",
        "999.999.999.999",
    ],
)
def test_mitre_lab_17_api_invalid_ip_returns_400_and_does_not_invoke_nmap(ip, monkeypatch):
    """Delta test: reject non-IP input and avoid command injection by not running subprocess."""

    from introduction import mitre

    # Fail the test if anything attempts to spawn a subprocess.
    def _boom(*args, **kwargs):
        raise AssertionError("subprocess was invoked for invalid IP")

    monkeypatch.setattr(mitre.subprocess, "Popen", _boom)

    class DummyReq:
        method = "POST"

        def __init__(self, ip_value):
            self.POST = {"ip": ip_value}

    resp = mitre.mitre_lab_17_api(DummyReq(ip))

    assert resp.status_code == 400
    assert b"Invalid IP address" in resp.content


def test_command_out_uses_popen_without_shell(monkeypatch):
    """Delta test: command_out must not use shell=True (argv list only)."""

    from introduction import mitre

    captured = {}

    class DummyProc:
        def communicate(self):
            return (b"ok", b"")

    def fake_popen(cmd, stdout=None, stderr=None, **kwargs):
        captured["cmd"] = cmd
        captured["kwargs"] = kwargs
        return DummyProc()

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    out, err = mitre.command_out(["nmap", "127.0.0.1"])

    assert out == b"ok"
    assert err == b""
    assert captured["cmd"] == ["nmap", "127.0.0.1"]
    assert "shell" not in captured["kwargs"], "shell must not be passed/enabled"
