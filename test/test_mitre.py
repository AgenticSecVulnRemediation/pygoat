import pytest


# Assumption: "introduction.mitre" is importable in tests.
from introduction import mitre


def test_mitre_lab_17_api_invalid_ip_returns_400(mocker):
    """Security regression: reject non-IP input instead of passing it to nmap."""
    # Arrange
    request = mocker.Mock()
    request.method = "POST"
    request.POST.get.return_value = "127.0.0.1; rm -rf /"

    command_out_spy = mocker.spy(mitre, "command_out")

    # Act
    response = mitre.mitre_lab_17_api(request)

    # Assert
    assert getattr(response, "status_code", None) == 400
    assert b"Invalid IP" in getattr(response, "content", b"")
    assert command_out_spy.call_count == 0


def test_mitre_lab_17_api_valid_ip_calls_command_out_with_list_and_shell_false(mocker):
    """Security regression: ensure command is executed without shell and with argv list."""
    # Arrange
    request = mocker.Mock()
    request.method = "POST"
    request.POST.get.return_value = "127.0.0.1"

    popen_mock = mocker.patch("introduction.mitre.subprocess.Popen")
    proc = mocker.Mock()
    proc.communicate.return_value = (b"STATE SERVICE\n\n80/tcp open http\n", b"")
    popen_mock.return_value = proc

    # Act
    mitre.mitre_lab_17_api(request)

    # Assert: command_out uses Popen(shell=False)
    popen_mock.assert_called_once()
    args, kwargs = popen_mock.call_args
    assert args[0] == ["nmap", "127.0.0.1"]
    assert kwargs.get("shell") is False
