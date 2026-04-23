import pytest
from django.http import HttpRequest

from introduction import views


class _DummyUser:
    def __init__(self, authenticated: bool = True):
        self.is_authenticated = authenticated


def _make_request(body: bytes) -> HttpRequest:
    req = HttpRequest()
    req.method = "POST"
    req.user = _DummyUser(True)
    req._body = body
    return req


def test_xxe_parse_uses_defusedxml_parser_rejects_entity(monkeypatch):
    """Delta test for switching to defusedxml.sax.make_parser: entity attacks should be blocked."""

    xml = b"""<?xml version='1.0'?>
    <!DOCTYPE foo [<!ENTITY xxe SYSTEM 'file:///etc/passwd'>]>
    <root><text>&xxe;</text></root>
    """

    request = _make_request(xml)

    response = views.xxe_parse(request)

    # defusedxml typically raises on entity declarations/usage; app should not succeed.
    assert response.status_code in (400, 500)
