import importlib
import os

import pytest


@pytest.mark.django_db
def test_ssrf_lab_rejects_encoded_path_traversal(rf, monkeypatch):
    """Regression test for path traversal mitigation.

    The fix URL-decodes the path, converts to absolute path, and ensures it
    remains under the intended directory.
    """

    views = importlib.import_module("introduction.views")

    # Make render deterministic by returning a simple HttpResponse containing the blog value
    def fake_render(_request, _template, context):
        from django.http import HttpResponse

        return HttpResponse(context.get("blog", ""))

    monkeypatch.setattr(views, "render", fake_render)

    request = rf.post("/ssrf/lab", {"blog": "..%2F..%2Fetc%2Fpasswd"})
    request.user = type("U", (), {"is_authenticated": True})()

    response = views.ssrf_lab(request)

    assert response.status_code == 200
    # On invalid traversal, the code should hit the exception path and return "No blog found"
    assert response.content.decode() == "No blog found"
