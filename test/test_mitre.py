import sys
import types

import pytest


def test_mitre_lab_17_api_builds_argv_list_for_nmap(monkeypatch):
    """Delta test: mitre_lab_17_api should build ['nmap', ip] (no string concatenation)."""

    # Arrange minimal django stubs
    shortcuts = types.ModuleType("django.shortcuts")
    shortcuts.redirect = lambda *a, **k: "redirect"
    shortcuts.render = lambda *a, **k: "render"

    class JsonResponse(dict):
        def __init__(self, data=None, status=200):
            super().__init__(data or {})
            self.status_code = status

    django_http = types.ModuleType("django.http")
    django_http.JsonResponse = JsonResponse
    django_http.HttpResponse = object
    django_http.HttpResponseBadRequest = object

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

    # Patch command_out to capture argv
    captured = {}

    def command_out_stub(cmd):
        captured["cmd"] = cmd
        # Must return bytes for decode()
        return (b"STATE SERVICE\n\n22/tcp open ssh\n", b"")

    sys.modules.pop("introduction.mitre", None)
    import introduction.mitre as mitre

    monkeypatch.setattr(mitre, "command_out", command_out_stub)

    class DummyRequest:
        method = "POST"

        class _POST:
            @staticmethod
            def get(key):
                assert key == "ip"
                return "127.0.0.1"

        POST = _POST()

    # Act
    resp = mitre.mitre_lab_17_api(DummyRequest())

    # Assert
    assert captured["cmd"] == ["nmap", "127.0.0.1"]
    assert "ports" in resp
