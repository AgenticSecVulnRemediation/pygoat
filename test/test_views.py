import io
import pytest


def _import_views_safely():
    """Import introduction.views without requiring a configured Django project.

    This test only needs the module object to verify that a9_lab calls yaml.safe_load.
    """
    try:
        import introduction.views as views
        return views
    except Exception:
        pytest.skip("Django environment not available; skipping unit-level import test")


def test_a9_lab_uses_yaml_safe_load(monkeypatch):
    views = _import_views_safely()

    called = {"safe": False}

    def safe_load_stub(stream):
        called["safe"] = True
        return {"ok": True}

    def load_should_not_be_called(*args, **kwargs):
        raise AssertionError("yaml.load should not be called; safe_load must be used")

    monkeypatch.setattr(views.yaml, "safe_load", safe_load_stub)
    monkeypatch.setattr(views.yaml, "load", load_should_not_be_called)

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        method = "POST"
        user = DummyUser()
        FILES = {"file": io.StringIO("k: v")}

    monkeypatch.setattr(views, "render", lambda request, template, context=None: context or {})

    result = views.a9_lab(DummyRequest())

    assert called["safe"] is True
    assert result["data"] == {"ok": True}
