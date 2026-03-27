import os
import pytest

# Assumptions:
# - introduction.playground.ssrf.main is importable.
# - We unit-test the changed behavior: absolute paths / traversal are rejected and function returns "No blog found".


def test_ssrf_lab_rejects_absolute_path_and_does_not_open(mocker):
    # Arrange
    from introduction.playground.ssrf import main

    open_mock = mocker.patch("builtins.open", side_effect=AssertionError("open() must not be called for invalid path"))

    # Act
    resp = main.ssrf_lab("/etc/passwd")

    # Assert
    assert resp == {"blog": "No blog found"}
    open_mock.assert_not_called()


def test_ssrf_lab_rejects_parent_traversal_and_does_not_open(mocker):
    # Arrange
    from introduction.playground.ssrf import main

    open_mock = mocker.patch("builtins.open", side_effect=AssertionError("open() must not be called for invalid path"))

    # Act
    resp = main.ssrf_lab("../secret.txt")

    # Assert
    assert resp == {"blog": "No blog found"}
    open_mock.assert_not_called()
