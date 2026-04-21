import os
import pytest

# Assumption: tests run with project root on PYTHONPATH so `introduction` is importable.
from introduction import views


class DummyUser:
    is_authenticated = True


class DummyRequest:
    def __init__(self, blog_value):
        self.user = DummyUser()
        self.method = "POST"
        self.POST = {"blog": blog_value}


def test_ssrf_lab_rejects_path_traversal_attempt(mocker):
    """Regression for path traversal fix: absolute paths / '..' must be rejected."""
    # Arrange: attempt to traverse out of allowed directory
    req = DummyRequest("../secret.txt")
    render_mock = mocker.patch.object(views, "render", return_value={"rendered": True})
    open_spy = mocker.patch("builtins.open", autospec=True)

    # Act
    views.ssrf_lab(req)

    # Assert
    # Should render error message, and must not try to open any file
    render_mock.assert_called()
    args, kwargs = render_mock.call_args
    assert kwargs.get("context") is None  # render called with positional context in this codebase
    # Context is 3rd positional argument
    assert args[2]["blog"] == "Invalid file path provided"
    open_spy.assert_not_called()


def test_ssrf_lab_rejects_absolute_path(mocker):
    req = DummyRequest(os.path.abspath("/tmp/real.txt"))
    render_mock = mocker.patch.object(views, "render", return_value={"rendered": True})
    open_spy = mocker.patch("builtins.open", autospec=True)

    views.ssrf_lab(req)

    args, _ = render_mock.call_args
    assert args[2]["blog"] == "Invalid file path provided"
    open_spy.assert_not_called()
