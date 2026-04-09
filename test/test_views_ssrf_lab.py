import pytest

# Assumption: module import path is introduction.views
import introduction.views as views


def test_views_ssrf_lab_rejects_path_traversal_before_open(mocker):
    # Arrange
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"
    request.POST = {"blog": "../secret.txt"}

    open_spy = mocker.patch('builtins.open')

    # Act / Assert
    with pytest.raises(ValueError, match="Invalid file path provided"):
        views.ssrf_lab(request)

    open_spy.assert_not_called()
