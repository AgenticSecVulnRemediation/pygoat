import os
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


def test_ssrf_lab_rejects_absolute_path(monkeypatch):
    # Arrange
    # If an attacker supplies an absolute path, it should be rejected before any open() attempt.
    request = _make_post_request("/etc/passwd")

    # Ensure that if open is called, we fail the test
    def _boom(*args, **kwargs):
        raise AssertionError("open() should not be called for absolute paths")

    monkeypatch.setattr(views, "open", _boom, raising=False)

    # Act
    response = views.ssrf_lab(request)

    # Assert: response should not include file contents; it returns the fallback message.
    assert response.status_code == 200
    assert b"No blog found" in response.content


def test_ssrf_lab_rejects_parent_directory_traversal(monkeypatch):
    # Arrange
    request = _make_post_request("../secret.txt")

    def _boom(*args, **kwargs):
        raise AssertionError("open() should not be called for traversal paths")

    monkeypatch.setattr(views, "open", _boom, raising=False)

    # Act
    response = views.ssrf_lab(request)

    # Assert
    assert response.status_code == 200
    assert b"No blog found" in response.content
