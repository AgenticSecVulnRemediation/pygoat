import pytest

# Assumption: tests run with project root on PYTHONPATH so `introduction` is importable.
from introduction import mitre


class DummyRequest:
    def __init__(self, method="POST", ip=None):
        self.method = method
        self.POST = {"ip": ip} if ip is not None else {}
        self.COOKIES = {}


def test_mitre_lab_17_api_rejects_invalid_ip_and_does_not_invoke_subprocess(mocker):
    """Regression for command injection fix: invalid IP must be rejected before calling nmap."""
    # Arrange
    req = DummyRequest(ip="127.0.0.1; rm -rf /")
    popen_spy = mocker.patch.object(mitre.subprocess, "Popen")

    # Act
    resp = mitre.mitre_lab_17_api(req)

    # Assert
    assert getattr(resp, "status_code", None) == 400
    assert b"Invalid IP" in resp.content
    popen_spy.assert_not_called()
