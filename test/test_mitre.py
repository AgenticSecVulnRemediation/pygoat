# Assumptions:
# - The project uses pytest.
# - The Django view functions in introduction.mitre can be tested as plain callables by providing a request-like object.

import pytest

from introduction import mitre


class _RequestStub:
    def __init__(self, method="POST", post=None):
        self.method = method
        self.POST = post or {}


def test_mitre_lab_17_api_rejects_invalid_ip_format(monkeypatch):
    """Delta test: invalid IP should return 400 and not attempt nmap."""

    def _boom(*args, **kwargs):
        raise AssertionError("command_out should not be called")

    monkeypatch.setattr(mitre, "command_out", _boom)

    req = _RequestStub(post={"ip": "8.8.8"})
    resp = mitre.mitre_lab_17_api(req)

    assert getattr(resp, "status_code", None) == 400
    assert b"Invalid IP address" in resp.content
