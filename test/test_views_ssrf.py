import types

import pytest

# Assumption: repository root is on PYTHONPATH in test runner.
from introduction import views


class _Req:
    def __init__(self, blog: str):
        self.method = "POST"
        self.POST = {"blog": blog}
        self.user = types.SimpleNamespace(is_authenticated=True)


def test_ssrf_lab_rejects_absolute_and_parent_traversal_paths(mocker):
    # Arrange
    render = mocker.patch.object(views, "render", autospec=True)

    # Act
    views.ssrf_lab(_Req("/etc/passwd"))
    views.ssrf_lab(_Req("../secrets.txt"))

    # Assert
    assert render.call_count == 2
    for call in render.call_args_list:
        assert call.args[1] == "Lab/ssrf/ssrf_lab.html"
        assert call.args[2] == {"blog": "Invalid file path provided"}


def test_ssrf_lab_rejects_paths_resolving_outside_views_dir(mocker):
    # Arrange
    render = mocker.patch.object(views, "render", autospec=True)

    # Simulate a normalized path escaping the base directory.
    mocker.patch.object(views.os.path, "dirname", return_value="/app/introduction")
    mocker.patch.object(views.os.path, "join", return_value="/app/introduction/ok/../../etc/passwd")
    mocker.patch.object(views.os.path, "normpath", return_value="/app/etc/passwd")

    # Act
    views.ssrf_lab(_Req("ok/../../etc/passwd"))

    # Assert
    render.assert_called_once()
    assert render.call_args.args[2] == {"blog": "Invalid file path provided"}
