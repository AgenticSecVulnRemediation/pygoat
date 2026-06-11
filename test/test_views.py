import importlib

import pytest


@pytest.mark.django_db
def test_ssrf_lab2_rejects_disallowed_domain(rf, monkeypatch):
    """Regression test for SSRF allowlist + scheme enforcement.

    The fix parses the URL and blocks requests unless scheme is http/https and
    hostname is in allowed_domains.
    """

    views = importlib.import_module("introduction.views")

    def fail_requests_get(*args, **kwargs):
        raise AssertionError("requests.get must not be called for disallowed URLs")

    monkeypatch.setattr(views.requests, "get", fail_requests_get)

    request = rf.post("/ssrf/lab2", {"url": "http://169.254.169.254/latest/meta-data/"})
    request.user = type("U", (), {"is_authenticated": True})()

    response = views.ssrf_lab2(request)

    assert response.status_code == 200
    assert b"URL not allowed" in response.content
