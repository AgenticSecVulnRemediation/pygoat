# Assumptions:
# - The Django app package is named `introduction` and is importable during tests.
# - We patch `render` to avoid Django template loading.

import io
import os
import types

import pytest


class _DummyUser:
    is_authenticated = True


class _DummyRequest:
    def __init__(self, blog_value):
        self.user = _DummyUser()
        self.method = "POST"
        self.POST = {"blog": blog_value}


def test_ssrf_lab_rejects_dotdot_traversal(monkeypatch):
    """Delta test for PR #1958: rejects '..' traversal attempt early."""
    import introduction.views as views

    rendered = {}

    def fake_render(_request, _template, context=None):
        rendered["context"] = context or {}
        return context

    monkeypatch.setattr(views, "render", fake_render)

    req = _DummyRequest("../secrets.txt")

    result = views.ssrf_lab(req)

    assert rendered["context"]["blog"] == "Invalid file path"
    assert result["blog"] == "Invalid file path"


def test_ssrf_lab_rejects_absolute_path(monkeypatch):
    """Delta test for PR #1958: rejects absolute path early."""
    import introduction.views as views

    rendered = {}

    def fake_render(_request, _template, context=None):
        rendered["context"] = context or {}
        return context

    monkeypatch.setattr(views, "render", fake_render)

    req = _DummyRequest("/etc/passwd")

    views.ssrf_lab(req)

    assert rendered["context"]["blog"] == "Invalid file path"
