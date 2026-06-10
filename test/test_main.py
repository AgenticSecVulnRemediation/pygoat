import os
import pytest

from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_absolute_paths_and_traversal(mocker):
    """Delta test: hardened SSRF file read must reject traversal/absolute paths and not open files."""

    # Arrange
    open_spy = mocker.patch("builtins.open", side_effect=AssertionError("open() must not be called for invalid path"))

    # Act
    result_traversal = ssrf_lab("../secrets.txt")
    result_abs = ssrf_lab(os.path.abspath("/etc/passwd"))

    # Assert
    assert result_traversal == {"blog": "No blog found"}
    assert result_abs == {"blog": "No blog found"}
    open_spy.assert_not_called()
