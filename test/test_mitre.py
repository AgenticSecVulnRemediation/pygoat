import pytest

from introduction import mitre


class _FakePopen:
    def __init__(self, args, shell, stdout, stderr):
        self.args = args
        self.shell = shell
        self.stdout = stdout
        self.stderr = stderr

    def communicate(self):
        # Minimal output that matches the regex used by mitre_lab_17_api
        out = (
            "Starting Nmap\n"
            "STATE SERVICE\n\n"
            "80/tcp open http\n"
        ).encode("utf-8")
        err = b""
        return out, err


def test_command_out_uses_shell_false(monkeypatch):
    # Arrange
    created = {}

    def fake_popen(args, shell, stdout, stderr):
        created["popen"] = _FakePopen(args, shell, stdout, stderr)
        return created["popen"]

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    # Act
    mitre.command_out(["nmap", "127.0.0.1"])

    # Assert
    assert created["popen"].shell is False


def test_mitre_lab_17_api_rejects_non_ip_input(monkeypatch):
    # Arrange
    class _Req:
        method = "POST"
        POST = {"ip": "127.0.0.1; rm -rf /"}

    # Avoid any subprocess execution if validation regresses
    def explode(*args, **kwargs):
        raise AssertionError("command_out should not be called for invalid IP")

    monkeypatch.setattr(mitre, "command_out", explode)

    # Act
    resp = mitre.mitre_lab_17_api(_Req())

    # Assert
    assert resp.status_code == 400
    assert b"Invalid IP address" in resp.content
