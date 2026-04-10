import os

# Assumption: module path is importable as introduction.playground.ssrf.main in test environment.
from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_absolute_path():
    # Arrange
    abs_path = os.path.abspath(__file__)

    # Act
    result = ssrf_lab(abs_path)

    # Assert
    assert result == {"blog": "Invalid file path provided."}


def test_ssrf_lab_rejects_parent_directory_traversal():
    # Arrange
    traversal = "../secrets.txt"

    # Act
    result = ssrf_lab(traversal)

    # Assert
    assert result == {"blog": "Invalid file path provided."}
