import pytest

from introduction import mitre


class _DummyRequest:
    def __init__(self, ip: str):
        self.method = "POST"
        self.POST = {"ip": ip}


def test_mitre_lab_17_api_rejects_non_ip_and_does_not_execute(mocker):
    """Regression test: invalid IP should return 400 before invoking nmap execution."""
    mock_command_out = mocker.patch.object(mitre, "command_out", autospec=True)

    # Use a command-injection style payload that previously would be concatenated into a shell command
    req = _DummyRequest("127.0.0.1; cat /etc/passwd")

    resp = mitre.mitre_lab_17_api(req)

    assert resp.status_code == 400
    mock_command_out.assert_not_called()
