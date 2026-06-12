import pytest


def test_a9_lab_uses_safe_load(monkeypatch):
    """Regression: a9_lab must use yaml.safe_load instead of yaml.load with Loader.

    We treat calling yaml.load as a security regression.
    """
    import introduction.views as views

    # Replace yaml module functions in views
    def unsafe_load(*args, **kwargs):
        raise AssertionError("yaml.load must not be used")

    captured = {}

    def safe_load(file_obj):
        captured["called"] = True
        return {"ok": True}

    monkeypatch.setattr(views.yaml, "load", unsafe_load)
    monkeypatch.setattr(views.yaml, "safe_load", safe_load)

    # Avoid django template rendering
    monkeypatch.setattr(views, "render", lambda _req, _tpl, ctx=None: ctx or {})

    class _Req:
        class user:
            is_authenticated = True

        method = "POST"

        FILES = {"file": object()}

    ctx = views.a9_lab(_Req())

    assert captured.get("called") is True
    assert ctx["data"] == {"ok": True}
