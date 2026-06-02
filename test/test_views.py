import os

import pytest


# Path derived from source file: introduction/views.py
from introduction import views


def test_ssrf_lab_rejects_absolute_or_parent_path_with_specific_message(mocker):
    # Arrange
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"

    render_mock = mocker.patch("introduction.views.render", return_value="resp")

    # absolute path
    request.POST = {"blog": os.path.abspath(__file__)}
    resp = views.ssrf_lab(request)
    assert resp == "resp"
    assert render_mock.call_args[0][2]["blog"] == "Invalid file path provided."

    # traversal
    request.POST = {"blog": "../x"}
    resp = views.ssrf_lab(request)
    assert resp == "resp"
    assert render_mock.call_args[0][2]["blog"] == "Invalid file path provided."
