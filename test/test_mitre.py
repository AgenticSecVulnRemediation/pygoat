import sys
import types

import pytest


def test_mitre_command_out_does_not_use_shell(monkeypatch):
    """Delta test: command_out must not pass shell=True to subprocess.Popen."""

    # Arrange: stub django and internal deps so mitre module can be imported.
    django_http = types.ModuleType("django.http")
    django_http.HttpResponse = object
    django_http.HttpResponseBadRequest = object

    class JsonResponse(dict):
        def __init__(self, data=None, status=200):
            super().__init__(data or {})
            self.status_code = status

    django_http.JsonResponse = JsonResponse

    shortcuts = types.ModuleType("django.shortcuts")
    shortcuts.redirect = lambda *a, **k: "redirect"
    shortcuts.render = lambda *a, **k: "render"

    csrf = types.ModuleType("django.views.decorators.csrf")
    csrf.csrf_exempt = lambda f: f

    models = types.ModuleType("introduction.models")
    models.CSRF_user_tbl = object

    views = types.ModuleType("introduction.views")
    views.authentication_decorator = lambda f: f

    monkeypatch.setitem(sys.modules, "django.http", django_http)
    monkeypatch.setitem(sys.modules, "django.shortcuts", shortcuts)
    monkeypatch.setitem(sys.modules, "django.views.decorators.csrf", csrf)
    monkeypatch.setitem(sys.modules, "introduction.models", models)
    monkeypatch.setitem(sys.modules, "introduction.views", views)

    popen_calls = []

    class DummyProcess:
        def communicate(self):
            return (b"", b"")

    def popen_spy(*args, **kwargs):
        popen_calls.append(kwargs)
        return DummyProcess()

    monkeypatch.setattr("subprocess.Popen", popen_spy)

    sys.modules.pop("introduction.mitre", None)
    import introduction.mitre as mitre

    # Act
    mitre.command_out(["nmap", "127.0.0.1"])

    # Assert
    assert popen_calls, "Expected subprocess.Popen to be invoked"
    assert "shell" not in popen_calls[0], "shell kwarg should not be set"
