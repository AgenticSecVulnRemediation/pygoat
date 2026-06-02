import subprocess

import pytest

from introduction import mitre


def test_mitre_lab_17_api_rejects_invalid_ip(monkeypatch):
    # Arrange
    class Req:
        method = 'POST'
        POST = {'ip': '127.0.0.1; rm -rf /'}

    # Ensure no subprocess execution is attempted
    def _boom(*args, **kwargs):
        raise AssertionError('subprocess should not be invoked for invalid IP')

    monkeypatch.setattr(subprocess, 'Popen', _boom)

    # Act
    resp = mitre.mitre_lab_17_api(Req())

    # Assert
    assert hasattr(resp, 'content')
    assert b'Invalid IP address' in resp.content
