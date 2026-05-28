# Assumption: 'introduction.views' is importable during tests and Django is configured.
# These tests focus ONLY on the security fix: path traversal / absolute path blocking in ssrf_lab.

import io

import pytest

import introduction.views as views


class _User:
    def __init__(self, authenticated: bool = True):
        self.is_authenticated = authenticated


class _Request:
    def __init__(self, blog_value: str, authenticated: bool = True):
        self.method = "POST"
        self.user = _User(authenticated)
        self.POST = {"blog": blog_value}


def test_ssrf_lab_blocks_absolute_paths(monkeypatch):
    # Arrange: make render deterministic
    def render_stub(_request, _template, context=None):
        return context or {}

    monkeypatch.setattr(views, "render", render_stub)

    # Ensure we would fail if file open is attempted
    def open_stub(*_args, **_kwargs):
        raise AssertionError("open() should not be called for invalid paths")

    monkeypatch.setattr(views, "open", open_stub, raising=False)

    req = _Request(blog_value="/etc/passwd")

    # Act
    ctx = views.ssrf_lab(req)

    # Assert
    assert ctx["blog"] == "Invalid file path"


@pytest.mark.parametrize(
    "payload",
    [
        "../secrets.txt",
        "..\\secrets.txt",
        "subdir/../../secrets.txt",
    ],
)
def test_ssrf_lab_blocks_path_traversal(monkeypatch, payload):
    # Arrange
    def render_stub(_request, _template, context=None):
        return context or {}

    monkeypatch.setattr(views, "render", render_stub)

    def open_stub(*_args, **_kwargs):
        raise AssertionError("open() should not be called for traversal attempts")

    monkeypatch.setattr(views, "open", open_stub, raising=False)

    req = _Request(blog_value=payload)

    # Act
    ctx = views.ssrf_lab(req)

    # Assert
    assert ctx["blog"] == "Invalid file path"
