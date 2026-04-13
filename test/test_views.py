import pytest

# Assumption: module is importable as introduction.views
import introduction.views as views


def test_ssrf_lab2_rejects_non_allowlisted_host_and_does_not_call_requests(monkeypatch):
    # Arrange
    request = type("Req", (), {})()
    request.user = type("User", (), {"is_authenticated": True})()
    request.method = "POST"
    request.POST = {"url": "http://127.0.0.1/"}

    called = {"count": 0}

    def fake_get(*args, **kwargs):
        called["count"] += 1
        raise AssertionError("requests.get must not be called for disallowed host")

    monkeypatch.setattr(views.requests, "get", fake_get)

    # Act
    resp = views.ssrf_lab2(request)

    # Assert
    assert b"Invalid URL" in resp.content
    assert called["count"] == 0
