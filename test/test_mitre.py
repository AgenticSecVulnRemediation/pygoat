import json

import pytest

import introduction.mitre as mitre


class _FakeProcess:
    def communicate(self):
        # Minimal output matching the regex used in mitre_lab_17_api
        stdout = b"STATE SERVICE\n\n22/tcp open ssh\n"
        stderr = b""
        return stdout, stderr


def test_mitre_lab_17_api_rejects_invalid_ip_address(mocker):
    request = mocker.Mock()
    request.method = "POST"
    request.POST = {"ip": "127.0.0.1; rm -rf /"}

    resp = mitre.mitre_lab_17_api(request)

    assert resp.status_code == 400
    body = json.loads(resp.content.decode())
    assert body["error"] == "Invalid IP address"


def test_mitre_lab_17_api_uses_list_command_without_shell(mocker):
    popen = mocker.patch('subprocess.Popen', autospec=True)
    popen.return_value = _FakeProcess()

    request = mocker.Mock()
    request.method = "POST"
    request.POST = {"ip": "127.0.0.1"}

    resp = mitre.mitre_lab_17_api(request)

    assert resp.status_code == 200

    # Ensure subprocess.Popen is invoked with a list command and without shell=True
    called_args, called_kwargs = popen.call_args
    assert called_args[0] == ["nmap", "127.0.0.1"]
    assert 'shell' not in called_kwargs or called_kwargs['shell'] is False
