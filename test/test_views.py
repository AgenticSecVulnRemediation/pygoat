import os

import pytest


# Path derived from source file: introduction/views.py
from introduction import views


def test_ssrf_lab_rejects_absolute_path_returns_invalid_file_path(mocker):
    # Arrange
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"
    request.POST = {"blog": os.path.abspath(__file__)}

    render_mock = mocker.patch("introduction.views.render", return_value="resp")

    # Act
    resp = views.ssrf_lab(request)

    # Assert
    assert resp == "resp"
    # second call arg is template name, third is context
    assert render_mock.call_args[0][1] == 'Lab/ssrf/ssrf_lab.html'
    assert render_mock.call_args[0][2]["blog"] == "Invalid file path"


def test_ssrf_lab_rejects_parent_traversal_returns_invalid_file_path(mocker):
    # Arrange
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"
    request.POST = {"blog": "../secrets.txt"}

    render_mock = mocker.patch("introduction.views.render", return_value="resp")

    # Act
    resp = views.ssrf_lab(request)

    # Assert
    assert resp == "resp"
    assert render_mock.call_args[0][2]["blog"] == "Invalid file path"
