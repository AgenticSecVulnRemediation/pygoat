import pytest

# Assumptions:
# - Module path is "introduction.mitre".
# - Delta: validate IP using ipaddress, and run subprocess with shell=False/list args.
from introduction import mitre


class _DummyRequest:
    def __init__(self, ip: str):
        self.method = "POST"
        self.POST = {"ip": ip}


def test_mitre_lab_17_api_rejects_non_ip_and_does_not_execute(monkeypatch):
    req = _DummyRequest("127.0.0.1; whoami")

    monkeypatch.setattr(mitre, "command_out", lambda *a, **k: (_ for _ in ()).throw(AssertionError("command_out must not be called")))

    resp = mitre.mitre_lab_17_api(req)
    assert getattr(resp, "status_code", None) == 400


def test_command_out_uses_shell_false(monkeypatch):
    popen_args = {}

    class _Proc:
        def communicate(self):
            return (b"out", b"")

    def _popen(cmd, **kwargs):
        popen_args.update({"cmd": cmd, **kwargs})
        return _Proc()

    monkeypatch.setattr(mitre.subprocess, "Popen", _popen)

    out, err = mitre.command_out(["nmap", "127.0.0.1"])
    assert out == b"out"
    assert err == b""
    assert popen_args.get("shell") is False
