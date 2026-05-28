import io

import pytest


def test_a9_lab_uses_safe_load(mocker):
    """Regression: YAML upload uses yaml.safe_load (not yaml.load with Loader)."""
    import introduction.views as views

    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"
    request.FILES = {"file": io.StringIO("a: 1\n")}

    safe_load = mocker.patch.object(views.yaml, "safe_load", return_value={"a": 1})
    load = mocker.patch.object(views.yaml, "load")

    # Patch render to avoid Django template engine; return a sentinel response
    sentinel = object()
    mocker.patch.object(views, "render", return_value=sentinel)

    resp = views.a9_lab(request)

    assert resp is sentinel
    safe_load.assert_called_once()
    load.assert_not_called()
