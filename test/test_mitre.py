import pytest


# Path derived from source file: introduction/mitre.py
from introduction import mitre


def test_mitre_lab_17_api_rejects_non_ip_input_returns_400(mocker):
    # Arrange
    req = mocker.Mock()
    req.method = "POST"
    req.POST = {"ip": "1.2.3.4; rm -rf /"}

    # Act
    resp = mitre.mitre_lab_17_api(req)

    # Assert
    assert resp.status_code == 400


def test_mitre_lab_17_api_uses_subprocess_without_shell_and_argument_list(mocker):
    # Arrange
    req = mocker.Mock()
    req.method = "POST"
    req.POST = {"ip": "127.0.0.1"}

    popen_mock = mocker.patch("introduction.mitre.subprocess.Popen")
    process = mocker.Mock()
    process.communicate.return_value = (b"STATE SERVICE\n\n80/tcp open http\n", b"")
    popen_mock.return_value = process

    # Act
    resp = mitre.mitre_lab_17_api(req)

    # Assert
    # Verify subprocess.Popen called with list args and no shell=True
    args, kwargs = popen_mock.call_args
    assert args[0] == ['nmap', '127.0.0.1']
    assert kwargs.get('shell') is None
    assert resp.status_code == 200
