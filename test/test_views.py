import os
import types

import pytest

import introduction.views as views


def test_ssrf_lab_blocks_path_traversal_outside_base_dir(monkeypatch):
    """Regression test for path traversal fix in ssrf_lab.

    Behavior change:
    - now the view rejects paths that resolve outside the module directory.
    """

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        user = DummyUser()
        method = "POST"
        POST = {"blog": "../settings.py"}

    # Make render() return its context for easy assertions
    def fake_render(_request, _template, context):
        return context

    monkeypatch.setattr(views, "render", fake_render)

    # Ensure abspath/dirname behave normally; we only assert outcome.
    context = views.ssrf_lab(DummyRequest())

    assert context["blog"] == "Invalid file path."
