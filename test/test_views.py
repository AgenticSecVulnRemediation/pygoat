# Assumption: Django app module is named `introduction`.

import io


def test_a9_lab_uses_yaml_safe_load(monkeypatch):
    """Delta test for insecure YAML load fix.

    Changed behavior: yaml.load(file, Loader) replaced with yaml.safe_load(file)
    to prevent unsafe object construction.
    """

    import introduction.views as views

    called = {"safe": 0}

    def _safe_load(file_obj):
        called["safe"] += 1
        return {"ok": True}

    # Patch the module's yaml.safe_load usage. The code calls yaml.safe_load(file).
    monkeypatch.setattr(views.yaml, "safe_load", _safe_load)

    # Ensure old dangerous API isn't used.
    def _load_should_not_be_called(*args, **kwargs):
        raise AssertionError("yaml.load should not be called after the fix")

    monkeypatch.setattr(views.yaml, "load", _load_should_not_be_called)

    # Avoid template rendering
    monkeypatch.setattr(views, "render", lambda request, tpl, ctx=None: (tpl, ctx))

    class DummyRequest:
        user = type("U", (), {"is_authenticated": True})()
        method = "POST"
        FILES = {"file": io.BytesIO(b"a: 1\n")}

    # Act
    tpl, ctx = views.a9_lab(DummyRequest())

    # Assert
    assert called["safe"] == 1
    assert ctx == {"data": {"ok": True}}
