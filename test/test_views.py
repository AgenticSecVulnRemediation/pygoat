import pytest
from django.http import HttpRequest

from introduction import views


class _DummyUser:
    def __init__(self, authenticated: bool = True):
        self.is_authenticated = authenticated


def _make_post_request(url: str) -> HttpRequest:
    req = HttpRequest()
    req.method = "POST"
    req.user = _DummyUser(True)
    req.POST = {"url": url}
    return req


def test_ssrf_lab2_rejects_non_allowlisted_host(monkeypatch):
    # Arrange
    request = _make_post_request("http://127.0.0.1:8000/")

    # Ensure outbound request isn't even attempted
    def _boom(*args, **kwargs):
        raise AssertionError("requests.get should not be called for unauthorized URL")

    monkeypatch.setattr(views.requests, "get", _boom)

    # Act
    response = views.ssrf_lab2(request)

    # Assert
    assert response.status_code == 200
    assert b"Invalid or unauthorized URL" in response.content
