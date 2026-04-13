import pytest

# Assumption: module is importable as introduction.mitre
from introduction import mitre


def test_command_out_invokes_subprocess_without_shell(monkeypatch):
    calls = {}

    class FakeProc:
        def communicate(self):
            return (b"ok", b"")

    def fake_popen(cmd, shell, stdout, stderr):
        calls["cmd"] = cmd
        calls["shell"] = shell
        calls["stdout"] = stdout
        calls["stderr"] = stderr
        return FakeProc()

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    out, err = mitre.command_out(["nmap", "127.0.0.1"])

    assert (out, err) == (b"ok", b"")
    assert calls["cmd"] == ["nmap", "127.0.0.1"]
    assert calls["shell"] is False
