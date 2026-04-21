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


def test_ssrf_lab_rejects_traversal_outside_allowed_dir(mocker):
    """Regression: ssrf_lab must not open files outside its directory."""
    req = DummyRequest("../secrets.txt")

    open_spy = mocker.patch("builtins.open", autospec=True)
    render_mock = mocker.patch.object(views, "render", return_value={"rendered": True})

    views.ssrf_lab(req)

    open_spy.assert_not_called()
    # called with context containing "No blog found" due to exception handler
    args, _ = render_mock.call_args
    assert args[2]["blog"] == "No blog found"


def test_ssrf_lab_allows_file_inside_allowed_dir(mocker, tmp_path):
    """Positive boundary: a safe relative path should be opened."""
    # Arrange: ensure dirname resolves and file exists under that dir
    # We patch os.path.dirname(__file__) usage by patching views.os.path.dirname
    allowed_dir = tmp_path
    (allowed_dir / "blog.txt").write_text("hi")

    req = DummyRequest("blog.txt")

    mocker.patch.object(views.os.path, "dirname", return_value=str(allowed_dir))
    render_mock = mocker.patch.object(views, "render", return_value={"rendered": True})

    # Act
    views.ssrf_lab(req)

    # Assert
    args, _ = render_mock.call_args
    assert args[2]["blog"] == "hi"
