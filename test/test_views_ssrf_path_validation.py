import os

import pytest


def test_ssrf_lab_rejects_absolute_and_traversal_paths(mocker):
    """Regression: ssrf_lab should short-circuit invalid file paths before attempting open()."""
    import introduction.views as views

    # Arrange
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"

    # Patch render to capture context
    def fake_render(_req, _tpl, ctx=None):
        resp = mocker.Mock()
        resp.context = ctx or {}
        return resp

    mocker.patch.object(views, "render", side_effect=fake_render)

    open_mock = mocker.patch("builtins.open")

    # Absolute path should be rejected
    request.POST = {"blog": os.path.abspath("/etc/passwd")}
    resp = views.ssrf_lab(request)
    assert resp.context["blog"] == "Invalid file path"

    # Traversal should be rejected
    request.POST = {"blog": "../secret.txt"}
    resp = views.ssrf_lab(request)
    assert resp.context["blog"] == "Invalid file path"

    open_mock.assert_not_called()
