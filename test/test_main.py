import os

import pytest

from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_absolute_paths():
    # Arrange
    abs_path = os.path.abspath(__file__)

    # Act
    result = ssrf_lab(abs_path)

    # Assert
    assert result == {"blog": "No blog found"}


def test_ssrf_lab_rejects_parent_directory_traversal():
    # Arrange
    traversal = "../secrets.txt"

    # Act
    result = ssrf_lab(traversal)

    # Assert
    assert result == {"blog": "No blog found"}
