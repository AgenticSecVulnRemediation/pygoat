import pytest

# Assumption: this module exists in the project
from introduction import views


def test_a9_lab_uses_yaml_safe_load_instead_of_yaml_load(mocker):
    """Delta test: ensures unsafe yaml.load is no longer used for uploaded YAML."""
    # Arrange
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"

    fake_file = mocker.Mock()
    request.FILES = {"file": fake_file}

    safe_load = mocker.patch("introduction.views.yaml.safe_load", return_value={"k": "v"})
    unsafe_load = mocker.patch("introduction.views.yaml.load", side_effect=AssertionError("yaml.load must not be called"))

    # Patch render to avoid needing templates and a full Django test setup
    render = mocker.patch("introduction.views.render", return_value=mocker.Mock(status_code=200, content=b""))

    # Act
    response = views.a9_lab(request)

    # Assert
    assert response.status_code == 200
    safe_load.assert_called_once_with(fake_file)
    unsafe_load.assert_not_called()
    render.assert_called_once()
