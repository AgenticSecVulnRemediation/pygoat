# Assumptions:
# - Repository uses pytest
# - Django is installed and configured for unit tests
# - The module is importable as introduction.mitre

import pytest


def test_mitre_lab_17_api_rejects_invalid_hostname_input(monkeypatch):
    """The fix validates the ip/hostname and rejects characters used in command injection."""
    import introduction.mitre as mitre

    class _Request:
        method = "POST"
        POST = {"ip": "127.0.0.1; cat /etc/passwd"}

    def explode_command_out(*args, **kwargs):
        raise AssertionError("command_out should not be called for invalid ip/hostname")

    monkeypatch.setattr(mitre, "command_out", explode_command_out)

    resp = mitre.mitre_lab_17_api(_Request())

    assert resp.status_code == 400
    assert b"Invalid IP address or hostname" in resp.content


def test_mitre_lab_17_api_calls_command_out_with_arg_list(monkeypatch):
    """The fix changes command construction to ['nmap', ip] (shell=False handled in command_out)."""
    import introduction.mitre as mitre

    class _Request:
        method = "POST"
        POST = {"ip": "127.0.0.1"}

    captured = {"command": None}

    def fake_command_out(command):
        captured["command"] = command
        fake_res = b"STATE SERVICE\n\n80/tcp open http\n"
        fake_err = b""
        return fake_res, fake_err

    monkeypatch.setattr(mitre, "command_out", fake_command_out)

    resp = mitre.mitre_lab_17_api(_Request())

    assert captured["command"] == ["nmap", "127.0.0.1"]
    assert resp.status_code == 200
    assert resp.json()["ports"] == ["80/tcp open http"]
