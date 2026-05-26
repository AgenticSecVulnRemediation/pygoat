import os
from types import SimpleNamespace

import pytest

# Assumption: Django project layout places source under 'introduction/' and tests under 'test/'.
# We mock render() to avoid needing Django test runner/templates.
import introduction.views as views


def _fake_authenticated_request(method="POST", post=None):
    return SimpleNamespace(
        method=method,
        POST=post or {},
        user=SimpleNamespace(is_authenticated=True),
    )


def test_ssrf_lab_rejects_path_traversal_outside_safe_blog_dir(monkeypatch, tmp_path):
    """Regression for path traversal fix in ssrf_lab: only allow reads from SAFE_BLOG_DIR."""
    # Arrange: point SAFE_BLOG_DIR to a temp dir and create an "outside" file.
    safe_dir = tmp_path / "safe_blogs"
    safe_dir.mkdir()
    outside_file = tmp_path / "outside.txt"
    outside_file.write_text("secret")

    monkeypatch.setattr(views, "SAFE_BLOG_DIR", str(safe_dir))

    captured = {}

    def fake_render(_request, template, context=None):
        captured["template"] = template
        captured["context"] = context or {}
        return captured

    monkeypatch.setattr(views, "render", fake_render)

    # Act: attempt traversal (would previously read arbitrary file).
    req = _fake_authenticated_request(post={"blog": "../outside.txt"})
    result = views.ssrf_lab(req)

    # Assert
    assert result["template"] == "Lab/ssrf/ssrf_lab.html"
    assert "blog" in result["context"]
    assert result["context"]["blog"] == "Access to the requested file is not allowed"


def test_ssrf_lab_reads_allowed_file_by_basename_only(monkeypatch, tmp_path):
    """Regression: legitimate blog files under SAFE_BLOG_DIR still load."""
    safe_dir = tmp_path / "safe_blogs"
    safe_dir.mkdir()
    (safe_dir / "post1.txt").write_text("hello")

    monkeypatch.setattr(views, "SAFE_BLOG_DIR", str(safe_dir))

    captured = {}

    def fake_render(_request, template, context=None):
        captured["template"] = template
        captured["context"] = context or {}
        return captured

    monkeypatch.setattr(views, "render", fake_render)

    req = _fake_authenticated_request(post={"blog": "post1.txt"})
    result = views.ssrf_lab(req)

    assert result["context"]["blog"] == "hello"
