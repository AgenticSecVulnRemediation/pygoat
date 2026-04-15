import types

import pytest

from introduction import views


def test_ssrf_lab_rejects_traversal_path_before_open(mocker):
    request = types.SimpleNamespace(
        user=types.SimpleNamespace(is_authenticated=True),
        method="POST",
        POST={"blog": "../secret.txt"},
    )

    render = mocker.patch.object(views, "render", return_value="RENDERED")
    open_spy = mocker.patch("builtins.open", side_effect=AssertionError("open should not be called"))

    resp = views.ssrf_lab(request)

    assert resp == "RENDERED"
    render.assert_called()
    open_spy.assert_not_called()
