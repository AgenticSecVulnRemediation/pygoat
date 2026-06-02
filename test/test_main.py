import os
import pytest

# Assumption: module is importable as introduction.playground.ssrf.main
from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_directory_traversal_returns_no_blog_found(tmp_path, monkeypatch):
    """Regression test for path traversal guard: absolute paths and '..' should be rejected."""
    # Arrange: make __file__ dirname point to a temp directory (avoid touching real repo files)
    fake_file = tmp_path / "main.py"
    fake_file.write_text("# sentinel")
    monkeypatch.setattr("introduction.playground.ssrf.main.__file__", str(fake_file))

    # Act
    result_parent = ssrf_lab("../secrets.txt")
    result_abs = ssrf_lab(str(tmp_path / "secrets.txt"))

    # Assert
    assert result_parent == {"blog": "No blog found"}
    assert result_abs == {"blog": "No blog found"}
