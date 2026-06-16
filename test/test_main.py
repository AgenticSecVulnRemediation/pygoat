import os
import pytest

from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_absolute_paths():
    # Arrange
    target = os.path.abspath(__file__)

    # Act
    result = ssrf_lab(target)

    # Assert
    assert result == {"blog": "No blog found"}


def test_ssrf_lab_rejects_parent_traversal_paths():
    # Arrange
    target = "../secrets.txt"

    # Act
    result = ssrf_lab(target)

    # Assert
    assert result == {"blog": "No blog found"}
