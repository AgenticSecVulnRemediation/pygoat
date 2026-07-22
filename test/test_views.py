import pytest


class _FakeRenderResult(dict):
    pass


class _FakeRequest:
    def __init__(self, blog_value):
        self.method = "POST"
        self.POST = {"blog": blog_value}
        self.user = type("User", (), {"is_authenticated": True})()


@pytest.fixture
def views_module(monkeypatch):
    """Import introduction.views with all Django/3rd-party dependencies mocked."""
    import sys
    import types

    # --- django stubs ---
    django = types.ModuleType("django")
    contrib = types.ModuleType("django.contrib")
    messages = types.ModuleType("django.contrib.messages")
    auth = types.ModuleType("django.contrib.auth")
    auth_forms = types.ModuleType("django.contrib.auth.forms")
    core = types.ModuleType("django.core")
    core_serializers = types.ModuleType("django.core.serializers")
    http = types.ModuleType("django.http")
    shortcuts = types.ModuleType("django.shortcuts")
    template = types.ModuleType("django.template")
    template_loader = types.ModuleType("django.template.loader")
    views_decorators = types.ModuleType("django.views")
    csrf = types.ModuleType("django.views.decorators")
    csrf_csrf = types.ModuleType("django.views.decorators.csrf")

    def _identity_decorator(fn):
        return fn

    csrf_csrf.csrf_exempt = _identity_decorator

    def _render(request, template_name, context=None):
        r = _FakeRenderResult()
        r["template"] = template_name
        r["context"] = context or {}
        return r

    def _redirect(name):
        return {"redirect": name}

    shortcuts.render = _render
    shortcuts.redirect = _redirect

    template_loader.render_to_string = lambda *a, **k: ""
    template.loader = template_loader

    http.HttpResponse = object
    http.HttpResponseBadRequest = object
    http.JsonResponse = object

    auth.authenticate = lambda *a, **k: None
    auth.login = lambda *a, **k: None
    auth_forms.UserCreationForm = object

    # wire modules
    sys.modules.update(
        {
            "django": django,
            "django.contrib": contrib,
            "django.contrib.messages": messages,
            "django.contrib.auth": auth,
            "django.contrib.auth.forms": auth_forms,
            "django.core": core,
            "django.core.serializers": core_serializers,
            "django.http": http,
            "django.shortcuts": shortcuts,
            "django.template": template,
            "django.template.loader": template_loader,
            "django.views": views_decorators,
            "django.views.decorators": csrf,
            "django.views.decorators.csrf": csrf_csrf,
        }
    )

    # --- other 3rd-party stubs used at import time ---
    sys.modules.setdefault("jwt", types.ModuleType("jwt"))

    # requests exists, but isn't used for this test
    import requests as real_requests

    sys.modules["requests"] = real_requests

    # argon2
    argon2 = types.ModuleType("argon2")
    argon2.PasswordHasher = object
    sys.modules["argon2"] = argon2

    # PIL
    pil = types.ModuleType("PIL")
    pil_image = types.ModuleType("PIL.Image")
    pil_imagemath = types.ModuleType("PIL.ImageMath")
    pil_image.Image = object
    sys.modules.update({"PIL": pil, "PIL.Image": pil_image, "PIL.ImageMath": pil_imagemath})

    # requests.structures
    requests_structures = types.ModuleType("requests.structures")
    requests_structures.CaseInsensitiveDict = dict
    sys.modules["requests.structures"] = requests_structures

    # local app imports
    intro_forms = types.ModuleType("introduction.forms")
    intro_forms.NewUserForm = object
    intro_models = types.ModuleType("introduction.models")
    # Provide attributes referenced during import
    for name in [
        "FAANG",
        "AF_admin",
        "AF_session_id",
        "Blogs",
        "CF_user",
        "authLogin",
        "comments",
        "info",
        "login",
        "otp",
        "sql_lab_table",
        "tickits",
    ]:
        setattr(intro_models, name, object)
    intro_utility = types.ModuleType("introduction.utility")
    intro_utility.customHash = lambda x: x
    intro_utility.filter_blog = lambda x: x

    sys.modules.update(
        {
            "introduction.forms": intro_forms,
            "introduction.models": intro_models,
            "introduction.utility": intro_utility,
            "pygoat.settings": types.ModuleType("pygoat.settings"),
        }
    )
    sys.modules["pygoat.settings"].SECRET_COOKIE_KEY = "secret"

    import importlib

    return importlib.import_module("introduction.views")


def test_ssrf_lab_rejects_parent_directory_traversal(views_module):
    # Arrange: typical traversal payload
    req = _FakeRequest(blog_value="../settings.py")

    # Act / Assert: fix introduces a hard failure for invalid paths
    with pytest.raises(Exception) as exc:
        views_module.ssrf_lab(req)

    assert "Invalid file path" in str(exc.value)


def test_ssrf_lab_rejects_absolute_path(views_module):
    # Arrange
    req = _FakeRequest(blog_value="/etc/passwd")

    # Act / Assert
    with pytest.raises(Exception) as exc:
        views_module.ssrf_lab(req)

    assert "Invalid file path" in str(exc.value)
