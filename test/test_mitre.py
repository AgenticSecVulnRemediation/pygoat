import datetime

import pytest

from introduction import mitre


class DummyPost:
    def __init__(self, ip):
        self._ip = ip

    def get(self, key):
        assert key == 'ip'
        return self._ip


class DummyRequest:
    method = 'POST'

    def __init__(self, ip):
        self.POST = DummyPost(ip)


def test_mitre_lab_17_api_rejects_invalid_ip(monkeypatch):
    # Arrange: ensure command_out is never reached for invalid IP
    def fail_command_out(_):
        raise AssertionError('command_out should not be called for invalid IP')

    monkeypatch.setattr(mitre, 'command_out', fail_command_out)

    request = DummyRequest('127.0.0.1; rm -rf /')

    # Act
    resp = mitre.mitre_lab_17_api(request)

    # Assert
    assert resp.status_code == 400


def test_mitre_lab_17_api_calls_command_out_with_list(monkeypatch):
    # Arrange
    called = {}

    def fake_command_out(cmd):
        called['cmd'] = cmd
        # Return a minimal nmap-like output that satisfies parsing
        out = b"STATE SERVICE\n\n80/tcp open http\n\n"
        err = b""
        return out, err

    monkeypatch.setattr(mitre, 'command_out', fake_command_out)
    request = DummyRequest('127.0.0.1')

    # Act
    resp = mitre.mitre_lab_17_api(request)

    # Assert: ensure list form is used (no shell string concatenation)
    assert called['cmd'] == ['nmap', '127.0.0.1']
    assert resp.status_code == 200
