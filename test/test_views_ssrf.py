import os
import pytest


def test_ssrf_lab_rejects_absolute_path(monkeypatch):
    """Delta: ssrf_lab now blocks absolute paths and returns an 'Invalid file path.' message."""
    from introduction import views

    class DummyRequest:
        def __init__(self, file_value):
            self.user = type("User", (), {"is_authenticated": True})()
            self.method = "POST"
            self.POST = {"blog": file_value}

    # Avoid template rendering; return context for assertions.
    def fake_render(_req, _tmpl, context=None):
        return context

    monkeypatch.setattr(views, "render", fake_render)

    ctx = views.ssrf_lab(DummyRequest("/etc/passwd"))
    assert ctx == {"blog": "Invalid file path."}


def test_ssrf_lab_rejects_path_escape(monkeypatch, tmp_path):
    """Delta: ssrf_lab checks abspath stays within dirname and rejects escapes."""
    from introduction import views

    # Make dirname a temp directory
    module_dir = tmp_path / "mod"
    module_dir.mkdir()
    monkeypatch.setattr(views.os.path, "dirname", lambda _p: str(module_dir))

    class DummyRequest:
        def __init__(self, file_value):
            self.user = type("User", (), {"is_authenticated": True})()
            self.method = "POST"
            self.POST = {"blog": file_value}

    def fake_render(_req, _tmpl, context=None):
        return context

    monkeypatch.setattr(views, "render", fake_render)

    # Provide a path that would escape if joined
    ctx = views.ssrf_lab(DummyRequest("../outside.txt"))
    assert ctx == {"blog": "Invalid file path."}
