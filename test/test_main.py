import os
import pytest

# Assumption: module path is importable as introduction.playground.ssrf.main
from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_path_traversal_dotdot():
    # Arrange
    malicious = "../secrets.txt"

    # Act
    result = ssrf_lab(malicious)

    # Assert
    assert result == {"blog": "No blog found"}


def test_ssrf_lab_rejects_absolute_path(tmp_path):
    # Arrange
    malicious = os.path.abspath(str(tmp_path / "x.txt"))

    # Act
    result = ssrf_lab(malicious)

    # Assert
    assert result == {"blog": "No blog found"}
