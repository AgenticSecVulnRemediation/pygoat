import pytest


from introduction import views


def test_a9_lab_uses_safe_load_not_load(mocker):
    """Regression for unsafe YAML loading: ensure yaml.safe_load is used."""
    # Arrange
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"
    request.FILES = {"file": object()}

    safe_load_mock = mocker.patch("introduction.views.yaml.safe_load", return_value={"k": "v"})
    load_mock = mocker.patch("introduction.views.yaml.load", side_effect=AssertionError("yaml.load should not be called"))
    render_mock = mocker.patch("introduction.views.render", return_value=mocker.Mock())

    # Act
    views.a9_lab(request)

    # Assert
    safe_load_mock.assert_called_once_with(request.FILES["file"])
    assert load_mock.call_count == 0
    render_mock.assert_called_once()
