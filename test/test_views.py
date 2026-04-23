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


def test_xxe_parse_external_entities_disabled_does_not_expand(monkeypatch):
    """Regression test for XXE hardening: external entities should not be expanded."""

    # Arrange: a classic XXE payload. If external entities were enabled, it would try to resolve &xxe;
    # potentially reading local files or causing errors.
    xml = b"""<?xml version='1.0'?>
    <!DOCTYPE foo [<!ENTITY xxe SYSTEM 'file:///etc/passwd'>]>
    <root><text>&xxe;</text></root>
    """
    request = _make_request(xml)

    # Act
    response = views.xxe_parse(request)

    # Assert
    # With external entities disabled, parsing should fail or at least not expand into sensitive content.
    # The implementation wraps parseString in a try/except and returns 400 on parse failures.
    assert response.status_code == 400
