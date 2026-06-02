# Assumptions:
# - The project uses pytest.
# - introduction.views.ssrf_lab2 blocks non-approved URLs by scheme and netloc.

import pytest

from introduction import views


class _Req:
    def __init__(self, url: str):
        self.user = type("U", (), {"is_authenticated": True})()
        self.method = "POST"
        self.POST = {"url": url}


def test_ssrf_lab2_blocks_unapproved_netloc_and_does_not_call_requests(monkeypatch):
    def _boom(*args, **kwargs):
        raise AssertionError("requests.get must not be called for blocked URL")

    monkeypatch.setattr(views.requests, "get", _boom)

    # Make render deterministic: return context dict.
    monkeypatch.setattr(views, "render", lambda request, tpl, ctx=None: ctx)

    ctx = views.ssrf_lab2(_Req("http://127.0.0.1/admin"))

    assert ctx == {"error": "URL is not allowed"}


def test_ssrf_lab2_allows_approved_domain(monkeypatch):
    class _Resp:
        content = b"OK"

    monkeypatch.setattr(views.requests, "get", lambda url: _Resp())
    monkeypatch.setattr(views, "render", lambda request, tpl, ctx=None: ctx)

    ctx = views.ssrf_lab2(_Req("https://approved-domain.com/"))

    assert ctx == {"response": "OK"}
