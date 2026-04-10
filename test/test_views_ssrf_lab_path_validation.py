import pytest


def test_ssrf_lab_rejects_traversal_and_absolute_paths(monkeypatch):
    # Regression test: ssrf_lab should reject absolute paths and '..' traversal.
    from introduction import views

    class Req:
        user = type('U', (), {'is_authenticated': True})()
        method = 'POST'
        POST = {'blog': '../secrets.txt'}

    resp = views.ssrf_lab(Req())
    assert getattr(resp, 'status_code', None) == 400

    class Req2:
        user = type('U', (), {'is_authenticated': True})()
        method = 'POST'
        POST = {'blog': '/etc/passwd'}

    resp2 = views.ssrf_lab(Req2())
    assert getattr(resp2, 'status_code', None) == 400
