import os

import pytest

import introduction.views as views


def test_ssrf_lab_rejects_traversal_and_does_not_open(monkeypatch):
    """Regression test for directory traversal checks in ssrf_lab."""

    class DummyRequest:
        user = type("U", (), {"is_authenticated": True})()
        method = "POST"
        POST = {"blog": "../secrets.txt"}

    def open_should_not_be_called(*args, **kwargs):
        raise AssertionError("open() should not be called for traversal paths")

    monkeypatch.setattr(views, "open", open_should_not_be_called, raising=False)

    resp = views.ssrf_lab(DummyRequest())
    assert "Invalid file path" in resp.content.decode("utf-8")


def test_ssrf_lab_rejects_path_escaping_base_dir(monkeypatch):
    class DummyRequest:
        user = type("U", (), {"is_authenticated": True})()
        method = "POST"
        POST = {"blog": "blog.txt"}

    # Force join to produce an escaped path and ensure access denied is returned
    monkeypatch.setattr(os.path, "dirname", lambda _: "/base")
    monkeypatch.setattr(os.path, "join", lambda a, b: "/base/../etc/passwd")
    monkeypatch.setattr(os.path, "abspath", lambda p: "/etc/passwd" if p.endswith("passwd") else "/base")

    resp = views.ssrf_lab(DummyRequest())
    assert "Access denied" in resp.content.decode("utf-8")
