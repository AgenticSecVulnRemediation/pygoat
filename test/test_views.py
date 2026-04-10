import os
from unittest.mock import mock_open

import pytest


# Assumptions:
# - Django app module path is `introduction.views`.
# - We unit-test only the path traversal hardening added to `ssrf_lab`.


def _make_request(authenticated=True, method="POST", blog_value="readme.txt"):
    class _User:
        is_authenticated = authenticated

    class _Request:
        user = _User()
        method = method
        POST = {"blog": blog_value}

    return _Request()


def test_ssrf_lab_rejects_dotdot_path_traversal(monkeypatch):
    from introduction import views

    request = _make_request(blog_value="../secrets.txt")

    render_calls = []

    def fake_render(_request, template, context=None):
        render_calls.append((template, context))
        return {"template": template, "context": context}

    monkeypatch.setattr(views, "render", fake_render)

    result = views.ssrf_lab(request)

    assert result["template"] == "Lab/ssrf/ssrf_lab.html"
    assert result["context"]["blog"] == "Invalid file path"


def test_ssrf_lab_rejects_absolute_path(monkeypatch):
    from introduction import views

    request = _make_request(blog_value=os.path.abspath("/etc/passwd"))

    def fake_render(_request, template, context=None):
        return {"template": template, "context": context}

    monkeypatch.setattr(views, "render", fake_render)

    result = views.ssrf_lab(request)

    assert result["template"] == "Lab/ssrf/ssrf_lab.html"
    assert result["context"]["blog"] == "Invalid file path"


def test_ssrf_lab_denies_escape_outside_base_dir(monkeypatch):
    from introduction import views

    # Arrange: a relative path without '..' that still resolves outside dirname via join/abspath.
    # Example: if dirname is /app/introduction, joining "../outside.txt" would be blocked earlier.
    # So we simulate a tricky case by monkeypatching os.path.abspath to return an escaped path.
    request = _make_request(blog_value="safe.txt")

    def fake_render(_request, template, context=None):
        return {"template": template, "context": context}

    monkeypatch.setattr(views, "render", fake_render)

    real_abspath = views.os.path.abspath

    def fake_abspath(path):
        # For the computed filename, force it to look like it escaped the base dir.
        if path.endswith("safe.txt"):
            return "/tmp/escaped/safe.txt"
        return real_abspath(path)

    monkeypatch.setattr(views.os.path, "abspath", fake_abspath)

    result = views.ssrf_lab(request)

    assert result["template"] == "Lab/ssrf/ssrf_lab.html"
    assert result["context"]["blog"] == "Access Denied"
