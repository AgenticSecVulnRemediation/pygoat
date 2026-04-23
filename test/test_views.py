import pytest
from django.http import HttpRequest

from introduction import views


class _DummyUser:
    def __init__(self, authenticated: bool = True):
        self.is_authenticated = authenticated


def _make_post_request(blog_value: str) -> HttpRequest:
    req = HttpRequest()
    req.method = "POST"
    req.user = _DummyUser(True)
    req.POST = {"blog": blog_value}
    return req


def test_ssrf_lab_rejects_traversal_paths(monkeypatch):
    request = _make_post_request("../secrets.txt")

    def _boom(*args, **kwargs):
        raise AssertionError("open() should not be called when traversal is detected")

    monkeypatch.setattr(views, "open", _boom, raising=False)

    response = views.ssrf_lab(request)

    assert response.status_code == 200
    assert b"No blog found" in response.content
