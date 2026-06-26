import os

import pytest


from introduction import views


def test_ssrf_lab_blocks_path_traversal_outside_views_directory(mocker):
    """Regression for file read traversal: paths escaping safe_dir must not be read."""
    # Arrange
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"
    request.POST = {"blog": "../../etc/passwd"}

    safe_dir = "/safe/base"

    mocker.patch("introduction.views.os.path.dirname", return_value="/safe")
    mocker.patch("introduction.views.os.path.realpath", side_effect=lambda p: safe_dir if p == "/safe" else "/etc/passwd")
    mocker.patch("introduction.views.os.path.normpath", side_effect=os.path.normpath)
    mocker.patch("introduction.views.os.path.join", side_effect=os.path.join)

    open_mock = mocker.patch("builtins.open", side_effect=AssertionError("open should not be called"))
    render_mock = mocker.patch("introduction.views.render", return_value="rendered")

    # Act
    result = views.ssrf_lab(request)

    # Assert
    assert result == "rendered"
    open_mock.assert_not_called()
    render_mock.assert_called_once()
    assert render_mock.call_args[0][1] == "Lab/ssrf/ssrf_lab.html"
    assert render_mock.call_args[0][2] == {"blog": "No blog found"}


def test_ssrf_lab_reads_file_when_within_safe_dir(mocker):
    """Valid path under safe_dir should still be readable."""
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"
    request.POST = {"blog": "blog.txt"}

    safe_dir = "/safe/base"
    filepath = "/safe/base/blog.txt"

    mocker.patch("introduction.views.os.path.dirname", return_value="/safe")
    mocker.patch("introduction.views.os.path.realpath", side_effect=lambda p: safe_dir if p == "/safe" else filepath)
    mocker.patch("introduction.views.os.path.normpath", side_effect=os.path.normpath)
    mocker.patch("introduction.views.os.path.join", side_effect=os.path.join)

    f = mocker.mock_open(read_data="hello")
    open_mock = mocker.patch("builtins.open", f)
    render_mock = mocker.patch("introduction.views.render", return_value="rendered")

    result = views.ssrf_lab(request)

    assert result == "rendered"
    open_mock.assert_called_once_with(filepath, "r")
    render_mock.assert_called_once()
    assert render_mock.call_args[0][2] == {"blog": "hello"}
