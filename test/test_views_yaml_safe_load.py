import io
import pytest


def test_a9_lab_uses_safe_load(monkeypatch):
    """Regression for unsafe yaml.load -> yaml.safe_load change.

    Ensures yaml.load is not used and safe_load is invoked.
    """
    from introduction import views

    called = {"safe": False}

    def fake_safe_load(file_obj):
        called["safe"] = True
        return {"a": 1}

    def fail_load(*args, **kwargs):
        raise AssertionError("yaml.load should not be called")

    monkeypatch.setattr(views.yaml, "safe_load", fake_safe_load)
    monkeypatch.setattr(views.yaml, "load", fail_load)

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        user = DummyUser()
        method = "POST"
        FILES = {"file": io.BytesIO(b"a: 1\n")}

    # render is a Django shortcut; stub it to avoid Django test client dependency
    def fake_render(_req, _template, context=None):
        return context

    monkeypatch.setattr(views, "render", fake_render)

    context = views.a9_lab(DummyRequest())
    assert called["safe"] is True
    assert context["data"] == {"a": 1}
