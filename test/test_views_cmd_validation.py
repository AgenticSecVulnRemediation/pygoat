import pytest


def test_cmd_lab_rejects_invalid_domain(monkeypatch):
    """Regression for command injection fix: invalid domain must be rejected early."""
    from introduction import views

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        user = DummyUser()
        method = "POST"
        POST = {"domain": "example.com; rm -rf /", "os": "linux"}

    def fake_render(_req, _template, context=None):
        return context

    def fail_popen(*args, **kwargs):
        raise AssertionError("subprocess.Popen should not be invoked for invalid domain")

    monkeypatch.setattr(views, "render", fake_render)
    monkeypatch.setattr(views.subprocess, "Popen", fail_popen)

    ctx = views.cmd_lab(DummyRequest())
    assert ctx["output"] == "Invalid domain"
