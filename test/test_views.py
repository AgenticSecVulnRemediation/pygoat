import sys
import types
import importlib
import pytest


def _install_django_stubs(monkeypatch):
    """Install minimal Django stubs so introduction.views can be imported without Django installed."""
    django = types.ModuleType("django")
    contrib = types.ModuleType("django.contrib")
    contrib_messages = types.ModuleType("django.contrib.messages")
    contrib_auth = types.ModuleType("django.contrib.auth")
    contrib_auth_forms = types.ModuleType("django.contrib.auth.forms")
    core = types.ModuleType("django.core")
    core_serializers = types.ModuleType("django.core.serializers")
    http = types.ModuleType("django.http")
    shortcuts = types.ModuleType("django.shortcuts")
    template = types.ModuleType("django.template")
    template_loader = types.ModuleType("django.template.loader")
    views = types.ModuleType("django.views")
    views_csrf = types.ModuleType("django.views.decorators")
    views_csrf_sub = types.ModuleType("django.views.decorators.csrf")

    # Basic callables used by the module
    def _noop(*args, **kwargs):
        return (args, kwargs)

    contrib_messages.success = _noop
    contrib_messages.error = _noop
    contrib_auth.authenticate = _noop
    contrib_auth.login = _noop
    contrib_auth_forms.UserCreationForm = object

    core.serializers = core_serializers

    class _HttpResponse:
        def __init__(self, content=None, status=200):
            self.content = content
            self.status_code = status
            self.headers = {}

        def __setitem__(self, k, v):
            self.headers[k] = v

        def set_cookie(self, *args, **kwargs):
            pass

        def delete_cookie(self, *args, **kwargs):
            pass

    http.HttpResponse = _HttpResponse
    http.HttpResponseBadRequest = _HttpResponse
    http.JsonResponse = lambda data, status=200: {"json": data, "status": status}

    shortcuts.redirect = lambda url: {"redirect": url}
    shortcuts.render = lambda *args, **kwargs: {"render": True, "args": args, "kwargs": kwargs}

    template.loader = template_loader
    template_loader.render_to_string = lambda *args, **kwargs: "rendered"

    views_csrf_sub.csrf_exempt = lambda f: f

    monkeypatch.setitem(sys.modules, "django", django)
    monkeypatch.setitem(sys.modules, "django.contrib", contrib)
    monkeypatch.setitem(sys.modules, "django.contrib.messages", contrib_messages)
    monkeypatch.setitem(sys.modules, "django.contrib.auth", contrib_auth)
    monkeypatch.setitem(sys.modules, "django.contrib.auth.forms", contrib_auth_forms)
    monkeypatch.setitem(sys.modules, "django.core", core)
    monkeypatch.setitem(sys.modules, "django.core.serializers", core_serializers)
    monkeypatch.setitem(sys.modules, "django.http", http)
    monkeypatch.setitem(sys.modules, "django.shortcuts", shortcuts)
    monkeypatch.setitem(sys.modules, "django.template", template)
    monkeypatch.setitem(sys.modules, "django.template.loader", template_loader)
    monkeypatch.setitem(sys.modules, "django.views", views)
    monkeypatch.setitem(sys.modules, "django.views.decorators", views_csrf)
    monkeypatch.setitem(sys.modules, "django.views.decorators.csrf", views_csrf_sub)


def _install_project_stubs(monkeypatch):
    """Stub introduction.* local imports used by views.py"""
    intro_forms = types.ModuleType("introduction.forms")
    intro_forms.NewUserForm = object

    intro_models = types.ModuleType("introduction.models")
    # Provide dummy model classes/attributes referenced in module
    class _DummyManager:
        def filter(self, *args, **kwargs):
            return []

        def raw(self, *args, **kwargs):
            return []

        def first(self):
            return None

        def create(self, *args, **kwargs):
            return types.SimpleNamespace(comment="Default")

        def update(self, *args, **kwargs):
            return 1

        def all(self):
            return []

        def get(self, *args, **kwargs):
            raise Exception("not found")

    dummy = types.SimpleNamespace(objects=_DummyManager())

    # Names imported from .models in views.py
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
        setattr(intro_models, name, dummy)

    intro_utility = types.ModuleType("introduction.utility")
    intro_utility.customHash = lambda x: x
    intro_utility.filter_blog = lambda x: x

    monkeypatch.setitem(sys.modules, "introduction.forms", intro_forms)
    monkeypatch.setitem(sys.modules, "introduction.models", intro_models)
    monkeypatch.setitem(sys.modules, "introduction.utility", intro_utility)

    # pygoat.settings import used in views.py
    pygoat = types.ModuleType("pygoat")
    pygoat_settings = types.ModuleType("pygoat.settings")
    pygoat_settings.SECRET_COOKIE_KEY = "test-secret"
    monkeypatch.setitem(sys.modules, "pygoat", pygoat)
    monkeypatch.setitem(sys.modules, "pygoat.settings", pygoat_settings)


def test_xxe_parse_disables_external_general_entities(monkeypatch, mocker):
    """Regression test for XXE fix: feature_external_ges must be set to False."""
    _install_django_stubs(monkeypatch)
    _install_project_stubs(monkeypatch)

    # Import after stubbing dependencies
    views = importlib.import_module("introduction.views")

    # Patch parser + XML parsing used by xxe_parse
    parser_mock = mocker.Mock()
    make_parser_mock = mocker.patch.object(views, "make_parser", return_value=parser_mock)

    # Simulate parseString returning iterable and allow expandNode
    class _Doc(list):
        def expandNode(self, node):
            return None

    class _Node:
        tagName = "text"

        def toxml(self):
            return "<text>hello</text>"

    doc = _Doc([(views.START_ELEMENT, _Node())])
    mocker.patch.object(views, "parseString", return_value=doc)

    # Patch DB update chain
    mock_comments = mocker.Mock()
    mock_comments.objects.filter.return_value.update.return_value = 1
    mocker.patch.object(views, "comments", mock_comments)

    # Patch render to avoid template lookup
    mocker.patch.object(views, "render", return_value={"render": True})

    request = types.SimpleNamespace(
        user=types.SimpleNamespace(is_authenticated=True),
        body=b"<root><text>hello</text></root>",
    )

    views.xxe_parse(request)

    make_parser_mock.assert_called_once()
    parser_mock.setFeature.assert_called_once_with(views.feature_external_ges, False)
