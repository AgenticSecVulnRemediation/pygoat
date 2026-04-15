import pytest

from introduction import mitre


class _DummyRequest:
    method = "POST"

    def __init__(self, ip):
        self._ip = ip

    @property
    def POST(self):
        return {"ip": self._ip}


def test_mitre_lab_17_api_rejects_invalid_ip_without_executing_subprocess(monkeypatch):
    # Arrange
    monkeypatch.setattr(
        mitre,
        "command_out",
        lambda _command: (_ for _ in ()).throw(AssertionError("command_out must not run")),
    )

    # Act
    resp = mitre.mitre_lab_17_api(_DummyRequest("1.2.3.4; rm -rf /"))

    # Assert
    assert resp.status_code == 400
    assert b"Invalid IP" in resp.content
