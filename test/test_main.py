import os

import pytest

from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_path_traversal_and_does_not_open(mocker):
    # Arrange
    open_spy = mocker.patch('builtins.open')

    # Act
    res = ssrf_lab('../secret.txt')

    # Assert
    assert res == {"blog": "No blog found"}
    open_spy.assert_not_called()


def test_ssrf_lab_rejects_absolute_path_and_does_not_open(mocker):
    # Arrange
    open_spy = mocker.patch('builtins.open')

    # Act
    res = ssrf_lab('/etc/passwd')

    # Assert
    assert res == {"blog": "No blog found"}
    open_spy.assert_not_called()
