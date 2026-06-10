import types
import pytest


import introduction.views as views


class _User:
    def __init__(self, authenticated: bool):
        self.is_authenticated = authenticated


class _Request:
    def __init__(self, authenticated: bool, blog_value: str):
        self.user = _User(authenticated)
        self.method = "POST"
        self.POST = {"blog": blog_value}


def test_ssrf_lab_rejects_path_traversal_before_file_open(mocker):
    """Regression test: path traversal in blog filename is rejected and open() is not reached."""

    # Arrange
    req = _Request(authenticated=True, blog_value="../../etc/passwd")

    open_spy = mocker.patch("builtins.open", side_effect=AssertionError("open() must not be called for traversal"))

    render_spy = mocker.patch.object(views, "render", return_value="rendered")

    # Act
    result = views.ssrf_lab(req)

    # Assert
    assert result == "rendered"
    open_spy.assert_not_called()

    # Ensure rendered with the specific invalid-path message
    args, kwargs = render_spy.call_args
    assert args[1] == "Lab/ssrf/ssrf_lab.html"
    assert kwargs["context_dict"].get("blog") == "Invalid file path provided." or args[2].get("blog") == "Invalid file path provided."
