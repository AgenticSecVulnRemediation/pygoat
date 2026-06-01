import os

import pytest


# Assumption: Django app is named `introduction` and `ssrf_lab` lives in `introduction.views`.
# These tests are delta-focused on the newly added path traversal protection.


def _make_fake_request(file_value: str):
    class _User:
        is_authenticated = True

    class _Req:
        method = "POST"
        user = _User()
        POST = {"blog": file_value}

    return _Req()


def test_ssrf_lab_rejects_absolute_path(monkeypatch):
    from introduction import views

    # Arrange: ensure any accidental file open would fail the test if called
    def _fail_open(*args, **kwargs):
        raise AssertionError("open() should not be called for invalid paths")

    monkeypatch.setattr(views, "open", _fail_open, raising=False)

    # Render returns a response; we only care that it returns early with our error message
    monkeypatch.setattr(views, "render", lambda request, template, ctx=None: ctx or {})

    req = _make_fake_request("/etc/passwd")

    # Act
    ctx = views.ssrf_lab(req)

    # Assert
    assert ctx["blog"].lower().startswith("invalid file path")


def test_ssrf_lab_rejects_parent_traversal(monkeypatch):
    from introduction import views

    monkeypatch.setattr(views, "render", lambda request, template, ctx=None: ctx or {})

    def _fail_open(*args, **kwargs):
        raise AssertionError("open() should not be called for traversal")

    monkeypatch.setattr(views, "open", _fail_open, raising=False)

    req = _make_fake_request("../../../../etc/passwd")

    ctx = views.ssrf_lab(req)

    assert "invalid file path" in ctx["blog"].lower()


def test_ssrf_lab_rejects_normalized_traversal(monkeypatch):
    from introduction import views

    monkeypatch.setattr(views, "render", lambda request, template, ctx=None: ctx or {})

    def _fail_open(*args, **kwargs):
        raise AssertionError("open() should not be called for traversal")

    monkeypatch.setattr(views, "open", _fail_open, raising=False)

    # os.path.normpath('../x') startswith('..') => reject
    req = _make_fake_request("a/../../secret.txt")

    ctx = views.ssrf_lab(req)

    assert "invalid file path" in ctx["blog"].lower()
