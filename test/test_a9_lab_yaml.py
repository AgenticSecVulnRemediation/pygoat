import io

import pytest


# Assumptions:
# - pytest is used.
# - We can import the Django view module directly.
# - We stub django.shortcuts.render to avoid Django setup.


def _make_authenticated_post_request(file_obj):
    class _User:
        is_authenticated = True

    class _Req:
        user = _User()
        method = "POST"
        FILES = {"file": file_obj}

    return _Req()


def test_a9_lab_uses_yaml_safe_load_instead_of_load(mocker):
    """Regression: YAML parsing should use yaml.safe_load (prevents unsafe object construction)."""
    from introduction import views

    # Arrange
    # Fail the test if yaml.load is called.
    mocker.patch.object(views.yaml, "load", side_effect=AssertionError("yaml.load must not be used"))
    safe_load = mocker.patch.object(views.yaml, "safe_load", return_value={"k": "v"})
    render = mocker.patch.object(views, "render", return_value="RESPONSE")

    fake_file = io.BytesIO(b"k: v")
    req = _make_authenticated_post_request(fake_file)

    # Act
    resp = views.a9_lab(req)

    # Assert
    assert resp == "RESPONSE"
    safe_load.assert_called_once()
    # ensure rendered context includes parsed data
    assert any("k" in str(arg) for arg in render.call_args[0])
