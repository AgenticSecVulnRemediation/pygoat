import pytest

# Assumption: module is importable as introduction.views
import introduction.views as views


def test_ssrf_lab_rejects_traversal_and_does_not_open_file(monkeypatch):
    # Arrange
    request = type("Req", (), {})()
    request.user = type("User", (), {"is_authenticated": True})()
    request.method = "POST"
    request.POST = {"blog": "../secret.txt"}

    opened = {"called": False}

    def fake_open(*args, **kwargs):
        opened["called"] = True
        raise AssertionError("open() must not be called for traversal")

    monkeypatch.setattr(views, "open", fake_open, raising=False)

    # Act
    resp = views.ssrf_lab(request)

    # Assert
    # Django render() returns HttpResponse; verify it rendered the rejection message
    assert b"Invalid file path" in resp.content
    assert opened["called"] is False


def test_ssrf_lab_rejects_absolute_path_and_does_not_open_file(monkeypatch):
    # Arrange
    request = type("Req", (), {})()
    request.user = type("User", (), {"is_authenticated": True})()
    request.method = "POST"
    request.POST = {"blog": "/etc/passwd"}

    opened = {"called": False}

    def fake_open(*args, **kwargs):
        opened["called"] = True
        raise AssertionError("open() must not be called for absolute path")

    monkeypatch.setattr(views, "open", fake_open, raising=False)

    # Act
    resp = views.ssrf_lab(request)

    # Assert
    assert b"Invalid file path" in resp.content
    assert opened["called"] is False
