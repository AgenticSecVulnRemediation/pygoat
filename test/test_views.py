import os
import types

import pytest

# Assumption: module path is importable as introduction.views
from introduction import views


def _make_request(blog_value):
    user = types.SimpleNamespace(is_authenticated=True)
    req = types.SimpleNamespace()
    req.method = "POST"
    req.POST = {"blog": blog_value}
    req.user = user
    return req


def test_ssrf_lab_candidate_path_must_stay_within_dir(monkeypatch):
    # Arrange
    req = _make_request("../secrets.txt")

    def fail_open(*args, **kwargs):
        raise AssertionError("open() must not be called for traversal")

    monkeypatch.setattr(views, "open", fail_open, raising=False)

    # Act
    resp = views.ssrf_lab(req)

    # Assert
    assert "No blog found" in str(resp.content)
