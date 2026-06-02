# Assumptions:
# - The project uses pytest.
# - introduction.views.ssrf_lab validates file paths to prevent traversal.

import os

import pytest

from introduction import views


class _Req:
    def __init__(self, blog: str):
        self.user = type("U", (), {"is_authenticated": True})()
        self.method = "POST"
        self.POST = {"blog": blog}


def test_ssrf_lab_blocks_traversal_and_does_not_open(monkeypatch):
    # If open is reached, fail the test.
    def _boom(*args, **kwargs):
        raise AssertionError("open must not be called for traversal attempt")

    monkeypatch.setattr(views, "open", _boom, raising=False)

    monkeypatch.setattr(views, "render", lambda request, tpl, ctx=None: ctx)

    ctx = views.ssrf_lab(_Req("../secret.txt"))

    assert ctx == {"blog": "Invalid file path"}
