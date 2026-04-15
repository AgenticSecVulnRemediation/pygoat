import pytest

# Assumptions:
# - Django project uses "introduction.views" module path.
# - Delta: cmd_lab validates domain and uses subprocess with shell=False/list args.
from introduction import views


class _DummyUser:
    is_authenticated = True


class _DummyRequest:
    def __init__(self, domain: str, os_value: str = "linux"):
        self.user = _DummyUser()
        self.method = "POST"
        self.POST = {"domain": domain, "os": os_value}


def test_cmd_lab_blocks_shell_injection_by_rejecting_invalid_domain(monkeypatch):
    req = _DummyRequest("example.com; whoami")

    monkeypatch.setattr(views, "render", lambda request, tpl, context=None: {"tpl": tpl, "ctx": context})
    monkeypatch.setattr(
        views.subprocess,
        "Popen",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("Popen should not be called for invalid domain")),
    )

    resp = views.cmd_lab(req)
    assert resp["ctx"]["output"] == "Invalid domain"
