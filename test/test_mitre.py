import importlib

import pytest
from django.http import HttpResponseBadRequest


@pytest.mark.django_db
def test_mitre_lab_17_api_rejects_non_ip_address(rf, monkeypatch):
    """Regression test for command injection mitigation.

    The fix validates the IP format and returns 400 before invoking nmap.
    """

    mitre = importlib.import_module("introduction.mitre")

    # Ensure command_out is not called for invalid input
    called = {"value": False}

    def fake_command_out(_cmd):
        called["value"] = True
        return b"", b""

    monkeypatch.setattr(mitre, "command_out", fake_command_out)

    request = rf.post("/mitre/17/api", {"ip": "127.0.0.1; rm -rf /"})
    response = mitre.mitre_lab_17_api(request)

    assert isinstance(response, HttpResponseBadRequest)
    assert response.status_code == 400
    assert called["value"] is False
