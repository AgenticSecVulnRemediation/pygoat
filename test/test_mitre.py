import re
import subprocess

import pytest

# Assumption: module is importable as introduction.mitre (Django app layout)
import introduction.mitre as mitre


def test_mitre_lab_17_api_rejects_invalid_ip_and_does_not_execute_command(mocker):
    # Arrange
    request = mocker.Mock()
    request.method = "POST"
    request.POST = {"ip": "127.0.0.1; rm -rf /"}

    popen_spy = mocker.patch.object(subprocess, "Popen")

    # Act
    response = mitre.mitre_lab_17_api(request)

    # Assert
    assert getattr(response, "status_code", None) == 400
    popen_spy.assert_not_called()


def test_mitre_lab_17_api_uses_argument_list_for_nmap_not_shell_string(mocker):
    # Arrange
    request = mocker.Mock()
    request.method = "POST"
    request.POST = {"ip": "127.0.0.1"}

    # Ensure we don't execute anything; stub command_out and parsing
    mocker.patch.object(mitre, "command_out", return_value=(b"STATE SERVICE\n\n22/tcp open ssh\n", b""))
    mocker.patch.object(re, "findall", return_value=["STATE SERVICE\n\n22/tcp open ssh\n"])

    # Act
    response = mitre.mitre_lab_17_api(request)

    # Assert
    assert getattr(response, "status_code", 200) == 200
    mitre.command_out.assert_called_once()
    (cmd,), _ = mitre.command_out.call_args
    assert cmd == ["nmap", "127.0.0.1"]
