import types

import pytest

# Assumption: module path is importable as introduction.mitre
from introduction import mitre


def _make_request(ip_value):
    req = types.SimpleNamespace()
    req.method = "POST"
    req.POST = {"ip": ip_value}
    req.COOKIES = {}
    return req


def test_mitre_lab_17_api_rejects_ip_not_matching_ipv4_regex(monkeypatch):
    # Arrange
    req = _make_request("127.0.0.1;whoami")
    monkeypatch.setattr(mitre, "command_out", lambda cmd: (b"", b""))

    # Act
    resp = mitre.mitre_lab_17_api(req)

    # Assert
    assert resp.status_code == 400


def test_mitre_lab_17_api_passes_list_to_command_out(monkeypatch):
    # Arrange
    req = _make_request("127.0.0.1")
    seen = {}

    def fake_command_out(cmd):
        seen["cmd"] = cmd
        # minimal output to satisfy regex in handler
        return (b"STATE SERVICE\n\n80/tcp open http\n", b"")

    monkeypatch.setattr(mitre, "command_out", fake_command_out)

    # Act
    resp = mitre.mitre_lab_17_api(req)

    # Assert
    assert seen["cmd"] == ["nmap", "127.0.0.1"]
    assert resp.status_code == 200
