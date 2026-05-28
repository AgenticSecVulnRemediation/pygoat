# Assumptions:
# - Repository uses pytest
# - Django is installed and configured for unit tests
# - The views module is importable as introduction.views

import pytest


def test_ssrf_lab2_rejects_disallowed_scheme_and_domain(monkeypatch):
    """The fix adds scheme/host allowlisting before outbound requests to mitigate SSRF."""
    import introduction.views as views

    class _User:
        is_authenticated = True

    class _Request:
        user = _User()
        method = "POST"
        POST = {"url": "http://127.0.0.1/admin"}

    def fake_render(_request, _template, context=None, *args, **kwargs):
        return {"template": _template, "context": context or {}}

    monkeypatch.setattr(views, "render", fake_render)

    def explode_get(*args, **kwargs):
        raise AssertionError("requests.get should not be called for non-allowlisted URL")

    monkeypatch.setattr(views.requests, "get", explode_get)

    result = views.ssrf_lab2(_Request())

    assert result["template"] == "Lab/ssrf/ssrf_lab2.html"
    assert result["context"]["error"] == "URL is not allowed"


def test_ssrf_lab2_allows_allowlisted_domain_and_makes_request(monkeypatch):
    """Allowlisted hostname + http/https should pass validation and execute requests.get."""
    import introduction.views as views

    class _User:
        is_authenticated = True

    class _Request:
        user = _User()
        method = "POST"
        POST = {"url": "https://trusted.example.com/path"}

    def fake_render(_request, _template, context=None, *args, **kwargs):
        return {"template": _template, "context": context or {}}

    monkeypatch.setattr(views, "render", fake_render)

    class _Resp:
        content = b"OK"

    called = {"url": None}

    def fake_get(url, *args, **kwargs):
        called["url"] = url
        return _Resp()

    monkeypatch.setattr(views.requests, "get", fake_get)

    result = views.ssrf_lab2(_Request())

    assert called["url"] == "https://trusted.example.com/path"
    assert result["template"] == "Lab/ssrf/ssrf_lab2.html"
    assert result["context"]["response"] == "OK"
