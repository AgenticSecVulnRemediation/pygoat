import os
import pytest


def test_ssrf_lab_blocks_path_traversal(monkeypatch):
    """Regression for path traversal fix in ssrf_lab.

    It should return 'No blog found' when traversal is attempted and must not open arbitrary files.
    """
    from introduction import views

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        user = DummyUser()
        method = "POST"
        POST = {"blog": "../../etc/passwd"}

    def fake_render(_req, _template, context=None):
        return context

    def fail_open(*args, **kwargs):
        raise AssertionError("open should not be called for traversal path")

    monkeypatch.setattr(views, "render", fake_render)
    monkeypatch.setattr(views, "open", fail_open, raising=False)

    ctx = views.ssrf_lab(DummyRequest())
    assert ctx["blog"] == "No blog found"
