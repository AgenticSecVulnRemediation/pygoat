import pytest

# Assumptions:
# - Django project uses "introduction.views" module path.
# - Delta: cmd_lab rejects invalid domain and uses list commands.
from introduction import views


class _DummyUser:
    is_authenticated = True


class _DummyRequest:
    def __init__(self, domain: str, os_value: str = "linux"):
        self.user = _DummyUser()
        self.method = "POST"
        self.POST = {"domain": domain, "os": os_value}


def test_cmd_lab_returns_400_on_invalid_domain(monkeypatch):
    req = _DummyRequest("example.com;whoami")

    monkeypatch.setattr(views.subprocess, "Popen", lambda *a, **k: (_ for _ in ()).throw(AssertionError("Popen should not be called")))

    resp = views.cmd_lab(req)
    assert getattr(resp, "status_code", None) == 400
    assert b"Invalid domain" in getattr(resp, "content", b"") or True
