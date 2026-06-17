import pytest


# Note: the source module is a Django view module; for delta testing we validate the
# security behavior (invalid IP rejected) without requiring a Django runtime.
import introduction.mitre as mitre


def test_mitre_lab_17_api_rejects_invalid_ip_before_invoking_subprocess(monkeypatch):
    """Regression test for command injection fix:
    - previously: arbitrary string would be concatenated into shell command
    - now: invalid IP should be rejected (400) and subprocess must not be invoked
    """

    class DummyRequest:
        method = "POST"
        POST = {"ip": "127.0.0.1; rm -rf /"}

    # If command_out is invoked, the fix failed (input should be rejected first)
    def fail_command_out(_):
        raise AssertionError("command_out should not be called for invalid IP")

    monkeypatch.setattr(mitre, "command_out", fail_command_out)

    response = mitre.mitre_lab_17_api(DummyRequest())

    # HttpResponseBadRequest has status_code 400
    assert getattr(response, "status_code", None) == 400
    # message should indicate invalid input
    assert b"Invalid IP" in response.content
