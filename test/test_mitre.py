import pytest

from introduction.mitre import mitre_lab_17_api


class _DummyRequest:
    def __init__(self, ip_value):
        self.method = "POST"
        self.POST = {"ip": ip_value}


def test_mitre_lab_17_api_rejects_invalid_ip(mocker):
    """Delta: IP address is now validated with ipaddress.ip_address and invalid input returns 400."""
    # Arrange: prevent any subprocess execution if validation is bypassed
    popen_spy = mocker.patch("introduction.mitre.subprocess.Popen")

    request = _DummyRequest("127.0.0.1; whoami")

    # Act
    response = mitre_lab_17_api(request)

    # Assert
    assert response.status_code == 400
    assert b"Invalid IP" in response.content
    popen_spy.assert_not_called()
