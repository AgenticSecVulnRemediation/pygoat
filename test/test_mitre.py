import types

import pytest

# Assumption: repository root is on PYTHONPATH in test runner.
from introduction import mitre


class _Req:
    def __init__(self, ip: str):
        self.method = "POST"
        self.POST = {"ip": ip}


def test_mitre_lab_17_api_rejects_invalid_ip(mocker):
    # Arrange
    req = _Req("127.0.0.1; rm -rf /")
    mocker.patch.object(mitre, "command_out", autospec=True)

    # Act
    resp = mitre.mitre_lab_17_api(req)

    # Assert
    assert resp.status_code == 400
    mitre.command_out.assert_not_called()


def test_mitre_lab_17_api_invokes_nmap_with_arg_list_not_shell_string(mocker):
    # Arrange
    req = _Req("127.0.0.1")

    # Ensure we never execute a real process
    command_out = mocker.patch.object(mitre, "command_out", autospec=True)
    # Minimal nmap output that satisfies the regex and parsing logic
    stdout = b"STATE SERVICE\n\n22/tcp open ssh\n"
    stderr = b""
    command_out.return_value = (stdout, stderr)

    # Act
    resp = mitre.mitre_lab_17_api(req)

    # Assert
    assert resp.status_code == 200
    (args, kwargs) = command_out.call_args
    assert args[0] == ["nmap", "127.0.0.1"]
    assert "ports" in resp.json()
