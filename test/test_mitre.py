import pytest


def test_mitre_lab_17_api_rejects_invalid_ip(monkeypatch):
    """Regression test for command injection fix: invalid IPs must be rejected.

    The fix added ipaddress.ip_address validation and returns 400 before running nmap.
    """
    from introduction import mitre

    class DummyRequest:
        method = "POST"
        POST = {"ip": "1.2.3.4; rm -rf /"}

    # If validation fails correctly, command_out must not be called.
    def fail_if_called(_cmd):
        raise AssertionError("command_out should not be called for invalid IP")

    monkeypatch.setattr(mitre, "command_out", fail_if_called)

    response = mitre.mitre_lab_17_api(DummyRequest())
    assert getattr(response, "status_code", None) == 400
