import os

import pytest

# Assumption: Django app module path is introduction.views
import introduction.views as views


def test_ssrf_lab_rejects_path_traversal_and_absolute_paths(monkeypatch):
    # Arrange: stub render to return context for easy assertions
    def fake_render(request, template, context=None):
        return {"template": template, "context": context or {}}

    monkeypatch.setattr(views, "render", fake_render)

    class DummyRequest:
        def __init__(self, blog_value):
            self.method = "POST"
            self.POST = {"blog": blog_value}
            self.user = type("U", (), {"is_authenticated": True})()

    # Act + Assert: traversal
    resp = views.ssrf_lab(DummyRequest("../secrets.txt"))
    assert resp["context"]["blog"] == "Invalid file path"

    # Act + Assert: absolute path
    resp2 = views.ssrf_lab(DummyRequest(os.path.abspath("/etc/passwd")))
    assert resp2["context"]["blog"] == "Invalid file path"
