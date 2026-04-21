import types

import pytest
import yaml

# Assumption: module path is importable as introduction.views
from introduction import views


def _make_request(file_obj):
    user = types.SimpleNamespace(is_authenticated=True)
    req = types.SimpleNamespace()
    req.method = "POST"
    req.FILES = {"file": file_obj}
    req.user = user
    return req


def test_a9_lab_uses_safe_load_rejects_python_object_tags(monkeypatch):
    # Arrange
    payload = "!!python/object/apply:os.system ['echo pwned']\n"
    file_obj = types.SimpleNamespace(read=lambda: payload.encode("utf-8"))

    # Avoid template rendering; ensure code reaches YAML parse and fails
    def fake_render(request, template, context=None):
        return types.SimpleNamespace(status_code=200, content=str(context).encode())

    monkeypatch.setattr(views, "render", fake_render)

    # Act
    resp = views.a9_lab(_make_request(file_obj))

    # Assert
    # safe_load should raise and the view should return context with data="Error"
    assert "'data': 'Error'" in resp.content.decode("utf-8")
