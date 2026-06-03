import json

import pytest


class _DummyRequest:
    def __init__(self, ip: str):
        self.method = "POST"
        self.POST = {"ip": ip}


def test_mitre_lab_17_api_rejects_invalid_ip_and_does_not_invoke_nmap(monkeypatch):
    """Delta: patched view checks valid_ip() and blocks invalid values."""

    from introduction import mitre

    called = {"count": 0}

    def _fake_command_out(_cmd_list):
        called["count"] += 1
        return (b"", b"")

    monkeypatch.setattr(mitre, "command_out", _fake_command_out)

    resp = mitre.mitre_lab_17_api(_DummyRequest("example.com"))

    assert resp.status_code == 400
    assert called["count"] == 0
