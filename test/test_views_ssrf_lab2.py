from types import SimpleNamespace

import pytest

import introduction.views as views


def _fake_authenticated_post(url_value):
    return SimpleNamespace(
        method="POST",
        POST={"url": url_value},
        user=SimpleNamespace(is_authenticated=True),
    )


def test_ssrf_lab2_rejects_untrusted_domain_before_requests_get(monkeypatch):
    """Regression for SSRF fix: deny non-allowlisted host/scheme and do not call requests.get."""

    def boom(_url):
        raise AssertionError("requests.get should not be called for rejected URLs")

    monkeypatch.setattr(views.requests, "get", boom)

    captured = {}

    def fake_render(_request, template, context=None):
        captured["template"] = template
        captured["context"] = context or {}
        return captured

    monkeypatch.setattr(views, "render", fake_render)

    resp = views.ssrf_lab2(_fake_authenticated_post("http://evil.example.com/"))

    assert resp["template"] == "Lab/ssrf/ssrf_lab2.html"
    assert resp["context"].get("error") == "Invalid URL"


def test_ssrf_lab2_allows_allowlisted_domain_and_calls_requests_get(monkeypatch):
    """Regression: allowlist host should pass validation and call requests.get."""
    seen = {}

    class _FakeResponse:
        content = b"ok"

    def fake_get(url):
        seen["url"] = url
        return _FakeResponse()

    monkeypatch.setattr(views.requests, "get", fake_get)

    captured = {}

    def fake_render(_request, template, context=None):
        captured["template"] = template
        captured["context"] = context or {}
        return captured

    monkeypatch.setattr(views, "render", fake_render)

    resp = views.ssrf_lab2(_fake_authenticated_post("https://safe.example.com/path"))

    assert seen["url"] == "https://safe.example.com/path"
    assert resp["context"].get("response") == "ok"
