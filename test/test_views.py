import importlib

import pytest


@pytest.mark.django_db
def test_ssrf_lab_rejects_absolute_path(rf, monkeypatch):
    """Regression test for normpath/isabs + commonprefix directory bound checks."""

    views = importlib.import_module("introduction.views")

    def fake_render(_request, _template, context):
        from django.http import HttpResponse

        return HttpResponse(context.get("blog", ""))

    monkeypatch.setattr(views, "render", fake_render)

    request = rf.post("/ssrf/lab", {"blog": "/etc/passwd"})
    request.user = type("U", (), {"is_authenticated": True})()

    response = views.ssrf_lab(request)

    assert response.status_code == 200
    assert response.content.decode() == "Invalid file path"
