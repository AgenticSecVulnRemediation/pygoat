import json

import pytest
from django.http import HttpResponseBadRequest


class _DummyRequest:
    def __init__(self, ip: str):
        self.method = "POST"
        self.POST = {"ip": ip}


def test_mitre_lab_17_api_rejects_injection_chars_returns_400(monkeypatch):
    """Delta: patched view validates ip/hostname and returns 400 for invalid input."""

    from introduction import mitre

    # Avoid spawning subprocess and parsing output; we should never reach it for invalid input.
    monkeypatch.setattr(mitre, "command_out", lambda _cmd: (b"", b""))

    resp = mitre.mitre_lab_17_api(_DummyRequest("127.0.0.1;rm -rf /"))

    assert isinstance(resp, HttpResponseBadRequest)
    assert "Invalid" in resp.content.decode("utf-8")
