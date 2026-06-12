# Assumptions:
# - Django project; we unit-test the view function directly with mocked request object.

import os
import types
import pytest


def _make_request(blog_value):
    return types.SimpleNamespace(
        user=types.SimpleNamespace(is_authenticated=True),
        method="POST",
        POST={"blog": blog_value},
    )


def test_ssrf_lab_blocks_absolute_paths(monkeypatch):
    from introduction import views

    # Arrange
    request = _make_request("/etc/passwd")

    # render should be invoked with an error message for invalid path
    def fake_render(_request, template, context):
        assert template.endswith("Lab/ssrf/ssrf_lab.html")
        assert context["blog"] == "Invalid file path provided."
        return (template, context)

    monkeypatch.setattr(views, "render", fake_render)

    # Act
    res = views.ssrf_lab(request)

    # Assert
    assert res[1]["blog"] == "Invalid file path provided."


def test_ssrf_lab_blocks_directory_traversal(monkeypatch):
    from introduction import views

    request = _make_request("../settings.py")

    def fake_render(_request, template, context):
        assert context["blog"] == "Invalid file path provided."
        return (template, context)

    monkeypatch.setattr(views, "render", fake_render)

    res = views.ssrf_lab(request)
    assert res[1]["blog"] == "Invalid file path provided."


def test_ssrf_lab_allows_normalized_relative_file(monkeypatch, tmp_path):
    from introduction import views

    # Arrange: create file under the views.py directory
    base_dir = os.path.dirname(views.__file__)
    target_rel = "safe_blog.txt"
    target_abs = os.path.join(base_dir, target_rel)
    with open(target_abs, "w", encoding="utf-8") as f:
        f.write("BLOG")

    request = _make_request(target_rel)

    def fake_render(_request, template, context):
        assert context["blog"] == "BLOG"
        return (template, context)

    monkeypatch.setattr(views, "render", fake_render)

    # Act
    res = views.ssrf_lab(request)

    # Assert
    assert res[1]["blog"] == "BLOG"
