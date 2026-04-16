import subprocess

import introduction.mitre as mitre


def test_mitre_lab_17_api_returns_400_for_invalid_ip_and_does_not_execute_command(monkeypatch):
    # Arrange
    popen_called = False

    def fake_popen(*args, **kwargs):
        nonlocal popen_called
        popen_called = True
        raise AssertionError('subprocess.Popen should not be called for invalid IP')

    monkeypatch.setattr(subprocess, 'Popen', fake_popen)

    class Req:
        method = 'POST'
        POST = {'ip': '999.999.999.999'}

    # Act
    resp = mitre.mitre_lab_17_api(Req())

    # Assert
    assert resp.status_code == 400
    assert popen_called is False
