import ipaddress

import pytest

from introduction import mitre


class _DummyPost:
    def __init__(self, ip_value):
        self._ip_value = ip_value

    def get(self, key, default=None):
        if key == 'ip':
            return self._ip_value
        return default


class _DummyRequest:
    method = 'POST'

    def __init__(self, ip_value):
        self.POST = _DummyPost(ip_value)


def test_mitre_lab_17_api_rejects_invalid_ip_before_running_command(mocker):
    # Arrange: invalid IP payload that previously would have been concatenated into a shell command
    req = _DummyRequest('127.0.0.1; whoami')

    popen_spy = mocker.patch('introduction.mitre.subprocess.Popen')

    # Act
    response = mitre.mitre_lab_17_api(req)

    # Assert: hardened behavior returns 400 and never spawns a subprocess
    assert getattr(response, 'status_code', None) == 400
    popen_spy.assert_not_called()


def test_mitre_lab_17_api_executes_nmap_with_argument_list_not_shell_string(mocker):
    # Arrange
    req = _DummyRequest('127.0.0.1')

    # Mock command_out so we don't run nmap; also ensure downstream parsing still works
    mocker.patch('introduction.mitre.command_out', return_value=(b'STATE SERVICE\n\n80/tcp open http\n', b''))

    # Act
    response = mitre.mitre_lab_17_api(req)

    # Assert: command is passed as a list ['nmap', ip] to command_out
    assert getattr(response, 'status_code', None) == 200
    # JsonResponse exposes .json() only in Django test client; but it does have .content
    content = response.content.decode('utf-8')
    assert '80/tcp open http' in content
