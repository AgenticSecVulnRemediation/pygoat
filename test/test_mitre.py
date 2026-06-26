import ipaddress

import pytest

# Assumption: introduction.mitre is importable in tests.
import introduction.mitre as mitre


def test_mitre_lab_17_api_rejects_invalid_ip_without_invoking_subprocess(monkeypatch):
    # Arrange
    called = {"count": 0}

    def fake_command_out(command):
        called["count"] += 1
        return (b"", b"")

    monkeypatch.setattr(mitre, "command_out", fake_command_out)

    class DummyPost:
        def __init__(self, ip):
            self._ip = ip

        def get(self, key):
            assert key == "ip"
            return self._ip

    class DummyRequest:
        method = "POST"

        def __init__(self, ip):
            self.POST = DummyPost(ip)

    # Act
    resp = mitre.mitre_lab_17_api(DummyRequest("127.0.0.1; rm -rf /"))

    # Assert
    assert resp.status_code == 400
    assert b"Invalid IP address" in resp.content
    assert called["count"] == 0
