import types

import pytest

# Assumption: module path is importable as introduction.views
from introduction import views


def _make_request(blog_value):
    user = types.SimpleNamespace(is_authenticated=True)
    req = types.SimpleNamespace()
    req.method = "POST"
    req.POST = {"blog": blog_value}
    req.user = user
    return req


def test_ssrf_lab_rejects_absolute_path(monkeypatch):
    # Arrange
    req = _make_request("/etc/passwd")

    def fail_open(*args, **kwargs):
        raise AssertionError("open() must not be called for invalid path")

    monkeypatch.setattr(views, "open", fail_open, raising=False)

    # Act
    resp = views.ssrf_lab(req)

    # Assert
    assert "Invalid file path provided" in str(resp.content)


def test_ssrf_lab_rejects_parent_directory_traversal(monkeypatch):
    # Arrange
    req = _make_request("../secrets.txt")

    def fail_open(*args, **kwargs):
        raise AssertionError("open() must not be called for traversal path")

    monkeypatch.setattr(views, "open", fail_open, raising=False)

    # Act
    resp = views.ssrf_lab(req)

    # Assert
    assert "Invalid file path provided" in str(resp.content)
