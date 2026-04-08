import io
import types
import pytest


# Assumption: Django app module path is introduction.views
# These tests focus only on the change from yaml.load(..., yaml.Loader) to yaml.safe_load(file).


def _make_request_with_file(user_authenticated=True, method="POST", file_bytes=b"a: 1\n"):
    user = types.SimpleNamespace(is_authenticated=user_authenticated)
    uploaded = io.BytesIO(file_bytes)
    # Django UploadedFile has .read(); BytesIO is sufficient for yaml.safe_load
    return types.SimpleNamespace(
        user=user,
        method=method,
        FILES={"file": uploaded},
    )


def test_a9_lab_uses_yaml_safe_load(monkeypatch):
    import introduction.views as views

    request = _make_request_with_file(file_bytes=b"a: 1\n")

    called = {"safe": 0, "unsafe": 0}

    def fake_safe_load(stream):
        called["safe"] += 1
        # Ensure it receives the uploaded file object
        assert hasattr(stream, "read")
        return {"a": 1}

    def fake_load(*args, **kwargs):
        called["unsafe"] += 1
        raise AssertionError("yaml.load should not be used")

    def fake_render(_request, template, context=None):
        return {"template": template, "context": context or {}}

    monkeypatch.setattr(views.yaml, "safe_load", fake_safe_load)
    monkeypatch.setattr(views.yaml, "load", fake_load)
    monkeypatch.setattr(views, "render", fake_render)

    result = views.a9_lab(request)

    assert called["safe"] == 1
    assert called["unsafe"] == 0
    assert result["context"]["data"] == {"a": 1}
