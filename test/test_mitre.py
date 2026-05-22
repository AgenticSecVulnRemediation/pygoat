import types
import pytest


def test_command_out_uses_shell_false_and_list_command(monkeypatch):
    """Regression test for OS command injection fix: shell must be disabled and argv list used."""
    import introduction.mitre as mitre

    captured = {}

    class DummyProc:
        def communicate(self):
            return (b"STATE SERVICE\n\n22/tcp open ssh\n", b"")

    def fake_popen(cmd, shell, stdout, stderr):
        captured["cmd"] = cmd
        captured["shell"] = shell
        return DummyProc()

    # Arrange: patch subprocess.Popen used by command_out
    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    # Act
    res, err = mitre.command_out(["nmap", "127.0.0.1"])

    # Assert
    assert captured["shell"] is False
    assert captured["cmd"] == ["nmap", "127.0.0.1"]
    assert isinstance(res, (bytes, bytearray))
    assert err == b""
