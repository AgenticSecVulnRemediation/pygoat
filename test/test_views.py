import os

import pytest

# Assumption: module is importable as introduction.views
import introduction.views as views


def test_ssrf_lab_rejects_absolute_path(monkeypatch):
    # Arrange
    opened = []

    def fake_open(*args, **kwargs):
        opened.append(args[0])
        raise AssertionError("open() should not be called for absolute paths")

    monkeypatch.setattr(views, "open", fake_open, raising=False)

    class _User:
        is_authenticated = True

    class _Request:
        user = _User()
        method = "POST"
        POST = {"blog": "/etc/passwd"}

    captured = {}

    def fake_render(_request, template, context=None):
        captured["template"] = template
        captured["context"] = context
        return context

    monkeypatch.setattr(views, "render", fake_render)

    # Act
    result = views.ssrf_lab(_Request())

    # Assert
    assert captured["template"] == "Lab/ssrf/ssrf_lab.html"
    assert result["blog"] == "Invalid file path"
    assert opened == []
