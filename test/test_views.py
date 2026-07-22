import sys
import types

import pytest


def test_a9_lab_uses_yaml_safe_load(monkeypatch):
    """Delta test: a9_lab should call yaml.safe_load(file) instead of yaml.load(file, yaml.Loader)."""

    # Arrange: stub django and other heavy deps so we can import introduction.views safely.
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
    http = types.ModuleType("django.http")

    class HttpResponse:  # minimal
        pass

    class HttpResponseBadRequest(Exception):
        pass

    class JsonResponse(dict):
        def __init__(self, data=None, status=200):
            super().__init__(data or {})
            self.status_code = status

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

    # Stub internal project modules used by introduction.views
    forms_mod = types.ModuleType("introduction.forms")
    forms_mod.NewUserForm = object
    models_mod = types.ModuleType("introduction.models")

    class DummyManager:
        def filter(self, *a, **k):
            return []

    # Provide only what's referenced when importing and in a9_lab
    models_mod.FAANG = types.SimpleNamespace(objects=DummyManager())
    models_mod.AF_admin = object
    models_mod.AF_session_id = object
    models_mod.Blogs = object
    models_mod.CF_user = object
    models_mod.authLogin = object
    models_mod.comments = types.SimpleNamespace(objects=types.SimpleNamespace(first=lambda: None, create=lambda **k: None, filter=lambda **k: types.SimpleNamespace(update=lambda **u: None)))
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

    # Stub yaml with safe_load spy
    yaml_mod = types.ModuleType("yaml")
    called = {"safe_load": 0, "load": 0}

    def safe_load(file_obj):
        called["safe_load"] += 1
        return {"ok": True}

    def load(*args, **kwargs):
        called["load"] += 1
        return {"bad": True}

    yaml_mod.safe_load = safe_load
    yaml_mod.load = load
    yaml_mod.Loader = object
    monkeypatch.setitem(sys.modules, "yaml", yaml_mod)

    # Ensure clean import after stubbing
    sys.modules.pop("introduction.views", None)
    import introduction.views as views

    class DummyRequest:
        user = types.SimpleNamespace(is_authenticated=True)
        method = "POST"
        FILES = {"file": object()}

    request = DummyRequest()

    # Act
    result = views.a9_lab(request)

    # Assert
    assert called["safe_load"] == 1
    assert called["load"] == 0
    assert result["context"]["data"] == {"ok": True}
