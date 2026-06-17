import pytest

import introduction.views as views


def test_ssrf_lab2_rejects_disallowed_scheme_or_host(monkeypatch):
    """Regression test for SSRF allowlist enforcement.

    Behavior change:
    - the handler now parses the URL and only allows http(s) to ALLOWED_HOSTS.
    """

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        method = "POST"
        POST = {"url": "http://evil.example.org/"}
        user = DummyUser()

    def fake_render(_request, _template, context):
        return context

    # requests.get must not be called when host is not allowed
    def fail_get(_):
        raise AssertionError("requests.get should not be called for disallowed host")

    monkeypatch.setattr(views, "render", fake_render)
    monkeypatch.setattr(views.requests, "get", fail_get)

    ctx = views.ssrf_lab2(DummyRequest())
    assert ctx == {"error": "URL not allowed"}
