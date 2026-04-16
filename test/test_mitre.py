import subprocess

import pytest

import introduction.mitre as mitre


def test_mitre_lab_17_api_rejects_invalid_ip_and_does_not_execute_command(monkeypatch):
    # Arrange: mock subprocess.Popen to ensure it's not called for invalid IP
    popen_called = False

    def fake_popen(*args, **kwargs):
        nonlocal popen_called
        popen_called = True
        raise AssertionError('subprocess.Popen should not be called for invalid IP')

    monkeypatch.setattr(subprocess, 'Popen', fake_popen)

    class Req:
        method = 'POST'
        POST = {'ip': '127.0.0.1; rm -rf /'}

    # Act / Assert
    with pytest.raises(ValueError):
        mitre.mitre_lab_17_api(Req())

    assert popen_called is False
