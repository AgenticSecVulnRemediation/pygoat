import sys
import types
import importlib
import pytest


def _install_django_stubs(monkeypatch):
    """Install minimal Django stubs so introduction.mitre can be imported without Django installed."""
    django = types.ModuleType("django")
    http = types.ModuleType("django.http")
    shortcuts = types.ModuleType("django.shortcuts")
    views = types.ModuleType("django.views")
    views_decorators = types.ModuleType("django.views.decorators")
    views_csrf = types.ModuleType("django.views.decorators.csrf")

    class _HttpResponse:
        def __init__(self, content=None, status=200):
            self.content = content
            self.status_code = status

    http.HttpResponse = _HttpResponse
    http.HttpResponseBadRequest = _HttpResponse
    http.JsonResponse = lambda data, status=200: {"json": data, "status": status}

    shortcuts.redirect = lambda url: {"redirect": url}
    shortcuts.render = lambda *args, **kwargs: {"render": True, "args": args, "kwargs": kwargs}

    views_csrf.csrf_exempt = lambda f: f

    monkeypatch.setitem(sys.modules, "django", django)
    monkeypatch.setitem(sys.modules, "django.http", http)
    monkeypatch.setitem(sys.modules, "django.shortcuts", shortcuts)
    monkeypatch.setitem(sys.modules, "django.views", views)
    monkeypatch.setitem(sys.modules, "django.views.decorators", views_decorators)
    monkeypatch.setitem(sys.modules, "django.views.decorators.csrf", views_csrf)


def _install_project_stubs(monkeypatch):
    intro_models = types.ModuleType("introduction.models")
    intro_models.CSRF_user_tbl = types.SimpleNamespace(objects=types.SimpleNamespace(filter=lambda **kwargs: []))

    intro_views = types.ModuleType("introduction.views")
    intro_views.authentication_decorator = lambda f: f

    monkeypatch.setitem(sys.modules, "introduction.models", intro_models)
    monkeypatch.setitem(sys.modules, "introduction.views", intro_views)


def test_mitre_lab_17_api_rejects_invalid_ip_and_does_not_execute_command(monkeypatch, mocker):
    _install_django_stubs(monkeypatch)
    _install_project_stubs(monkeypatch)

    mitre = importlib.import_module("introduction.mitre")

    # If IP validation fails, command_out must not run
    command_out_spy = mocker.patch.object(mitre, "command_out")

    request = types.SimpleNamespace(method="POST", POST={"ip": "8.8.8.8; rm -rf /"})
    resp = mitre.mitre_lab_17_api(request)

    assert hasattr(resp, "status_code")
    assert resp.status_code == 400
    command_out_spy.assert_not_called()


def test_mitre_lab_17_api_executes_nmap_without_shell_with_valid_ip(monkeypatch, mocker):
    _install_django_stubs(monkeypatch)
    _install_project_stubs(monkeypatch)

    mitre = importlib.import_module("introduction.mitre")

    # command_out should be called with list form: ['nmap', ip]
    mocker.patch.object(mitre, "command_out", return_value=(b"STATE SERVICE\n\n22/tcp open ssh\n", b""))

    # Make re.findall deterministic for our minimal output
    mocker.patch.object(mitre.re, "findall", return_value=["STATE SERVICE\n\n22/tcp open ssh\n"])

    request = types.SimpleNamespace(method="POST", POST={"ip": "127.0.0.1"})
    resp = mitre.mitre_lab_17_api(request)

    assert resp["status"] == 200
    assert resp["json"]["ports"] == ["22/tcp open ssh"]
    mitre.command_out.assert_called_once_with(["nmap", "127.0.0.1"])
