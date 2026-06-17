import pytest
from django.contrib.auth.models import AnonymousUser

# Assumption: project uses Django and this module exists at this import path
from introduction import views


def _make_request(blog_value: str):
    """Minimal request stub for ssrf_lab POST flow."""
    class Req:
        method = "POST"
        POST = {"blog": blog_value}
        user = AnonymousUser()
        user.is_authenticated = True

    return Req()


def test_ssrf_lab_rejects_dotdot_path_traversal_and_does_not_open_file(mocker):
    # Arrange: attempt traversal that previously would be joined and opened
    request = _make_request("../secret.txt")
    open_spy = mocker.patch("builtins.open", autospec=True)

    # Act
    response = views.ssrf_lab(request)

    # Assert: vulnerable file open is blocked and a safe response is returned
    open_spy.assert_not_called()
    assert response.status_code == 200
    # Rendered content should contain the new error message
    content = response.content.decode("utf-8")
    assert "Invalid file path" in content


def test_ssrf_lab_rejects_absolute_path_and_does_not_open_file(mocker):
    # Arrange
    request = _make_request("/etc/passwd")
    open_spy = mocker.patch("builtins.open", autospec=True)

    # Act
    response = views.ssrf_lab(request)

    # Assert
    open_spy.assert_not_called()
    assert response.status_code == 200
    assert "Invalid file path" in response.content.decode("utf-8")
