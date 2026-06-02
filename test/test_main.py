import os
import tempfile

import pytest


# Path derived from source file: introduction/playground/ssrf/main.py
from introduction.playground.ssrf import main


def test_ssrf_lab_rejects_absolute_path_and_returns_no_blog_found():
    # Arrange
    # Absolute paths should be rejected and handled by the broad exception -> No blog found
    abs_path = os.path.abspath(__file__)

    # Act
    result = main.ssrf_lab(abs_path)

    # Assert
    assert result == {"blog": "No blog found"}


def test_ssrf_lab_rejects_parent_traversal_and_returns_no_blog_found():
    # Arrange
    traversal = "../secret.txt"

    # Act
    result = main.ssrf_lab(traversal)

    # Assert
    assert result == {"blog": "No blog found"}


def test_ssrf_lab_allows_reading_file_within_directory():
    # Arrange
    # Create a file in the same directory as main.py
    base_dir = os.path.abspath(os.path.dirname(main.__file__))
    with tempfile.NamedTemporaryFile(mode="w", dir=base_dir, delete=False) as f:
        f.write("hello")
        filename = os.path.basename(f.name)

    try:
        # Act
        result = main.ssrf_lab(filename)

        # Assert
        assert result == {"blog": "hello"}
    finally:
        os.unlink(os.path.join(base_dir, filename))
