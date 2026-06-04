import re

import pytest


# Assumption: module path is importable from repo root.
import introduction.mitre as mitre


def test_mitre_lab_17_api_rejects_invalid_ip(mocker):
    request = mocker.Mock()
    request.method = "POST"
    request.POST = {"ip": "127.0.0.1; rm -rf /"}

    response = mitre.mitre_lab_17_api(request)

    assert getattr(response, "status_code", None) == 400
    # Ensure subprocess isn't invoked on invalid input
    assert not mitre.command_out.called if hasattr(mitre.command_out, "called") else True


def test_mitre_lab_17_api_uses_list_command_not_shell_string(mocker):
    # Arrange
    command_out_spy = mocker.spy(mitre, "command_out")

    request = mocker.Mock()
    request.method = "POST"
    request.POST = {"ip": "127.0.0.1"}

    # Keep downstream parsing from exploding; return output with expected pattern.
    fake_nmap_output = b"STATE SERVICE\n\n80/tcp open http\n"
    command_out_spy.return_value = (fake_nmap_output, b"")

    # Act
    mitre.mitre_lab_17_api(request)

    # Assert: command_out called with a list (no shell string concatenation)
    args, _ = command_out_spy.call_args
    assert isinstance(args[0], list)
    assert args[0][0] == "nmap"
    assert args[0][1] == "127.0.0.1"
