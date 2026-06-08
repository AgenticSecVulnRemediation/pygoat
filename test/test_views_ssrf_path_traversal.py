import pytest

# Assumption: Django view module is importable as introduction.views in this repo layout.
from introduction import views


class _DummyUser:
    is_authenticated = True


class _DummyRequest:
    def __init__(self, blog: str):
        self.method = "POST"
        self.user = _DummyUser()
        self.POST = {"blog": blog}


def test_ssrf_lab_rejects_path_traversal_and_does_not_open_file(mocker):
    """Regression test for traversal fix: path must be kept under views.py directory."""
    # Arrange
    mock_render = mocker.patch.object(views, "render", autospec=True)
    mock_open = mocker.patch("builtins.open", autospec=True)

    # Attempt to break out of the base directory
    req = _DummyRequest("../../../../etc/passwd")

    # Act
    views.ssrf_lab(req)

    # Assert
    mock_open.assert_not_called()
    mock_render.assert_called_once()
    assert mock_render.call_args.args[2]["blog"] == "Invalid file path"
