import os
from types import SimpleNamespace

import pytest


# Assumptions:
# - introduction.views can be imported without Django app initialization for this unit-level test.
# - We stub Django's render() and redirect() to avoid requiring templates/settings.


def test_ssrf_lab_blocks_path_traversal_and_returns_invalid_file_path_message(monkeypatch):
    """Regression test for path traversal guard added to ssrf_lab().

    Previously, user-controlled `blog` could include '..' or absolute paths and be joined into a filesystem path.
    The fix rejects these inputs early and returns a safe response.
    """

    import introduction.views as views

    # Arrange
    captured = {}

    def fake_render(request, template, context=None, *args, **kwargs):
        captured["template"] = template
        captured["context"] = context or {}
        return SimpleNamespace(template=template, context=context or {})

    monkeypatch.setattr(views, "render", fake_render)

    request = SimpleNamespace(
        user=SimpleNamespace(is_authenticated=True),
        method="POST",
        POST={"blog": "../secret.txt"},
    )

    # Act
    response = views.ssrf_lab(request)

    # Assert
    assert response.template == "Lab/ssrf/ssrf_lab.html"
    assert response.context == {"blog": "Invalid file path."}


@pytest.mark.parametrize("blog", ["/etc/passwd", os.path.abspath(__file__)])
def test_ssrf_lab_blocks_absolute_paths(monkeypatch, blog):
    import introduction.views as views

    captured = {}

    def fake_render(request, template, context=None, *args, **kwargs):
        captured["template"] = template
        captured["context"] = context or {}
        return SimpleNamespace(template=template, context=context or {})

    monkeypatch.setattr(views, "render", fake_render)

    request = SimpleNamespace(
        user=SimpleNamespace(is_authenticated=True),
        method="POST",
        POST={"blog": blog},
    )

    response = views.ssrf_lab(request)

    assert response.template == "Lab/ssrf/ssrf_lab.html"
    assert response.context == {"blog": "Invalid file path."}
