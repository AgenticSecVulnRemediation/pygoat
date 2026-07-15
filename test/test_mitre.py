import sys
import types
import pytest


@pytest.fixture(autouse=True)
def _mock_external_dependencies_before_import(monkeypatch):
    """Mock Django + project-level imports used by introduction.mitre.

    This keeps the test runnable even when Django isn't installed.
    """
    # ---- Minimal fake django modules ----
    django = types.ModuleType("django")
    http = types.ModuleType("django.http")
    shortcuts = types.ModuleType("django.shortcuts")
    views = types.ModuleType("django.views")
    views_decorators = types.ModuleType("django.views.decorators")
    csrf = types.ModuleType("django.views.decorators.csrf")

    class _Resp:
        def __init__(self, body=None, status=200):
            self.status_code = status
            self.content = (body or "").encode() if isinstance(body, str) else body

    def HttpResponseBadRequest(body=""):
        return _Resp(body=body, status=400)

    def JsonResponse(data):
        # keep it lightweight; we only need status_code
        return _Resp(body=str(data), status=200)

    def HttpResponse(body=""):
        return _Resp(body=body, status=200)

    http.HttpResponse = HttpResponse
    http.HttpResponseBadRequest = HttpResponseBadRequest
    http.JsonResponse = JsonResponse

    def redirect(_to):
        return _Resp(status=302)

    def render(_req, _tpl, _ctx=None):
        return _Resp(status=200)

    shortcuts.redirect = redirect
    shortcuts.render = render

    csrf.csrf_exempt = lambda f: f

    # Register in sys.modules so `import introduction.mitre` succeeds.
    sys.modules.setdefault("django", django)
    sys.modules.setdefault("django.http", http)
    sys.modules.setdefault("django.shortcuts", shortcuts)
    sys.modules.setdefault("django.views", views)
    sys.modules.setdefault("django.views.decorators", views_decorators)
    sys.modules.setdefault("django.views.decorators.csrf", csrf)

    # ---- Project-level relative imports ----
    models_mod = types.ModuleType("introduction.models")
    views_mod = types.ModuleType("introduction.views")

    # authentication_decorator should be no-op
    views_mod.authentication_decorator = lambda f: f

    class _FakeManager:
        def filter(self, **_kwargs):
            return []

    class _FakeTbl:
        objects = _FakeManager()

    models_mod.CSRF_user_tbl = _FakeTbl

    sys.modules.setdefault("introduction.models", models_mod)
    sys.modules.setdefault("introduction.views", views_mod)


class _FakePost:
    def __init__(self, values):
        self._values = values

    def get(self, k, default=None):
        return self._values.get(k, default)


class _FakeRequest:
    def __init__(self, method="POST", post=None):
        self.method = method
        self.POST = _FakePost(post or {})


def test_mitre_lab_17_api_with_invalid_ip_returns_400_and_does_not_invoke_nmap(monkeypatch):
    import introduction.mitre as mitre

    # Arrange: ensure nmap execution is never reached
    def _boom(_cmd):
        raise AssertionError("command_out should not be called for invalid IP")

    monkeypatch.setattr(mitre, "command_out", _boom, raising=True)

    req = _FakeRequest(post={"ip": "127.0.0.1; rm -rf /"})

    # Act
    resp = mitre.mitre_lab_17_api(req)

    # Assert
    assert getattr(resp, "status_code", None) == 400


def test_mitre_lab_17_api_with_valid_ip_passes_argv_list_to_command_out(monkeypatch):
    import introduction.mitre as mitre

    observed = {"cmd": None}

    def _fake_command_out(cmd):
        observed["cmd"] = cmd
        # Must satisfy regex parsing: contains "STATE SERVICE\n\n" followed by at least one line.
        stdout = b"Header\nSTATE SERVICE\n\n22/tcp open ssh\n"
        stderr = b""
        return stdout, stderr

    monkeypatch.setattr(mitre, "command_out", _fake_command_out, raising=True)

    req = _FakeRequest(post={"ip": "127.0.0.1"})

    resp = mitre.mitre_lab_17_api(req)

    assert observed["cmd"] == ["nmap", "127.0.0.1"]
    assert getattr(resp, "status_code", None) == 200
