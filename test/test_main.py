import os
from unittest.mock import mock_open

import pytest


# Assumption: ssrf_lab is defined in introduction/playground/ssrf/main.py
from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_with_absolute_path_raises_value_error(mocker):
    # Arrange
    mocker.patch("os.path.isabs", return_value=True)

    # Act / Assert
    with pytest.raises(ValueError, match="Invalid file path provided"):
        ssrf_lab("/etc/passwd")


def test_ssrf_lab_with_parent_traversal_raises_value_error(mocker):
    # Arrange
    mocker.patch("os.path.isabs", return_value=False)

    # Act / Assert
    with pytest.raises(ValueError, match="Invalid file path provided"):
        ssrf_lab("../secrets.txt")


def test_ssrf_lab_with_relative_filename_reads_file(mocker):
    # Arrange
    mocker.patch("os.path.isabs", return_value=False)
    mocker.patch("os.path.dirname", return_value="/app/introduction/playground/ssrf")
    mocker.patch("os.path.join", return_value="/app/introduction/playground/ssrf/blog.txt")
    m = mock_open(read_data="hello")
    mocker.patch("builtins.open", m)

    # Act
    result = ssrf_lab("blog.txt")

    # Assert
    assert result == {"blog": "hello"}
    m.assert_called_once_with("/app/introduction/playground/ssrf/blog.txt", "r")
