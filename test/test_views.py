import sys
import types

import pytest


def test_cmd_lab_uses_subprocess_without_shell(monkeypatch):
    """Delta test: cmd_lab should call subprocess.Popen with shell=False and an argv list."""

    # Arrange: minimal stubs to import views
    dummy = lambda *a, **k: None

    django = types.ModuleType("django")
    contrib = types.ModuleType("django.contrib")
    messages = types.ModuleType("django.contrib.messages")
    messages.success = dummy
    messages.error = dummy
    auth = types.ModuleType("django.contrib.auth")
    auth.authenticate = dummy
    auth.login = dummy
    auth_forms = types.ModuleType("django.contrib.auth.forms")
    auth_forms.UserCreationForm = object
    core = types.ModuleType("django.core")
    serializers = types.ModuleType("django.core.serializers")

    class HttpResponse:  # minimal
        pass

    class HttpResponseBadRequest(Exception):
        pass

    class JsonResponse(dict):
        def __init__(self, data=None, status=200):
            super().__init__(data or {})
            self.status_code = status

    http = types.ModuleType("django.http")
    http.HttpResponse = HttpResponse
    http.HttpResponseBadRequest = HttpResponseBadRequest
    http.JsonResponse = JsonResponse

    shortcuts = types.ModuleType("django.shortcuts")
    shortcuts.redirect = lambda *a, **k: "redirect"
    shortcuts.render = lambda request, template, context=None: {"template": template, "context": context}

    template = types.ModuleType("django.template")
    loader = types.ModuleType("django.template.loader")
    loader.render_to_string = lambda *a, **k: ""

    decorators = types.ModuleType("django.views.decorators")
    csrf = types.ModuleType("django.views.decorators.csrf")
    csrf.csrf_exempt = lambda f: f

    monkeypatch.setitem(sys.modules, "django", django)
    monkeypatch.setitem(sys.modules, "django.contrib", contrib)
    monkeypatch.setitem(sys.modules, "django.contrib.messages", messages)
    monkeypatch.setitem(sys.modules, "django.contrib.auth", auth)
    monkeypatch.setitem(sys.modules, "django.contrib.auth.forms", auth_forms)
    monkeypatch.setitem(sys.modules, "django.core", core)
    monkeypatch.setitem(sys.modules, "django.core.serializers", serializers)
    monkeypatch.setitem(sys.modules, "django.http", http)
    monkeypatch.setitem(sys.modules, "django.shortcuts", shortcuts)
    monkeypatch.setitem(sys.modules, "django.template", template)
    monkeypatch.setitem(sys.modules, "django.template.loader", loader)
    monkeypatch.setitem(sys.modules, "django.views.decorators", decorators)
    monkeypatch.setitem(sys.modules, "django.views.decorators.csrf", csrf)

    forms_mod = types.ModuleType("introduction.forms")
    forms_mod.NewUserForm = object
    models_mod = types.ModuleType("introduction.models")

    class DummyManager:
        def filter(self, *a, **k):
            return []

    models_mod.FAANG = types.SimpleNamespace(objects=DummyManager())
    models_mod.AF_admin = object
    models_mod.AF_session_id = object
    models_mod.Blogs = object
    models_mod.CF_user = object
    models_mod.authLogin = object
    models_mod.comments = object
    models_mod.info = object
    models_mod.login = types.SimpleNamespace(objects=DummyManager())
    models_mod.otp = object
    models_mod.sql_lab_table = object
    models_mod.tickits = object

    utility_mod = types.ModuleType("introduction.utility")
    utility_mod.customHash = lambda s: s
    utility_mod.filter_blog = lambda s: s

    monkeypatch.setitem(sys.modules, "introduction.forms", forms_mod)
    monkeypatch.setitem(sys.modules, "introduction.models", models_mod)
    monkeypatch.setitem(sys.modules, "introduction.utility", utility_mod)

    sys.modules.pop("introduction.views", None)
    import introduction.views as views

    popen_args = {}

    class DummyProc:
        def communicate(self):
            return (b"out", b"")

    def popen_stub(args, **kwargs):
        popen_args["args"] = args
        popen_args["kwargs"] = kwargs
        return DummyProc()

    monkeypatch.setattr(views.subprocess, "Popen", popen_stub)

    class DummyRequest:
        user = types.SimpleNamespace(is_authenticated=True)
        method = "POST"

        class _POST:
            @staticmethod
            def get(key):
                if key == "domain":
                    return "example.com"
                if key == "os":
                    return "win"
                raise KeyError(key)

        POST = _POST()

    # Act
    views.cmd_lab(DummyRequest())

    # Assert
    assert popen_args["args"] == ["nslookup", "example.com"]
    assert popen_args["kwargs"].get("shell") is False
