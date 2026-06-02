import pytest


# Path derived from source file: introduction/views.py
from introduction import views


def test_a9_lab_uses_yaml_safe_load_instead_of_load(mocker):
    # Arrange
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"
    request.FILES = {"file": mocker.Mock()}

    safe_load = mocker.patch("introduction.views.yaml.safe_load", return_value={"ok": True})
    load = mocker.patch("introduction.views.yaml.load", side_effect=AssertionError("yaml.load should not be used"))

    render_mock = mocker.patch("introduction.views.render", return_value="resp")

    # Act
    resp = views.a9_lab(request)

    # Assert
    assert resp == "resp"
    safe_load.assert_called_once()
    # If yaml.load is called, the test will fail via side_effect
    assert load.call_count == 0
