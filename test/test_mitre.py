import subprocess

import pytest


# NOTE: pytest-style unit tests for Django view helper logic in introduction/mitre.py.
# We avoid Django request/response wiring and focus only on the security-relevant
# change in how subprocess is invoked (no shell, argument list).


def test_command_out_does_not_use_shell(mocker):
    """Regression: command_out must not invoke subprocess with shell=True."""
    from introduction import mitre

    popen = mocker.patch('introduction.mitre.subprocess.Popen')
    popen.return_value.communicate.return_value = (b"ok", b"")

    mitre.command_out(["nmap", "127.0.0.1"])

    # Must not pass shell=True after fix.
    assert popen.call_args[1].get('shell') is None


def test_mitre_lab_17_api_rejects_invalid_ip_and_does_not_execute_command(mocker):
    """Regression: invalid IP should be rejected (400) and command must not execute."""
    from introduction import mitre

    # If the code attempts to execute, fail the test.
    mocker.patch('introduction.mitre.command_out', side_effect=AssertionError("command_out must not be called"))

    class _Req:
        method = "POST"
        POST = {'ip': '127.0.0.1; rm -rf /'}

    resp = mitre.mitre_lab_17_api(_Req())

    assert hasattr(resp, 'status_code')
    assert resp.status_code == 400
