import os

import pytest

# Assumption: function under test lives in introduction.playground.ssrf.main
from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_with_traversal_path_returns_no_blog_found(monkeypatch):
    """Regression test for the fix: path traversal input should not read files."""

    # Arrange: if open is called, fail the test (should be blocked before open)
    def _open(*args, **kwargs):
        raise AssertionError("open() must not be called for traversal paths")

    monkeypatch.setattr("builtins.open", _open)

    # Act
    result = ssrf_lab("../secret.txt")

    # Assert
    assert result == {"blog": "No blog found"}


def test_ssrf_lab_with_absolute_path_returns_no_blog_found(monkeypatch):
    """Regression test for the fix: absolute path input should not read files."""

    def _open(*args, **kwargs):
        raise AssertionError("open() must not be called for absolute paths")

    monkeypatch.setattr("builtins.open", _open)

    # Use an absolute path depending on platform
    abs_path = "C:/Windows/win.ini" if os.name == "nt" else "/etc/passwd"

    # Act
    result = ssrf_lab(abs_path)

    # Assert
    assert result == {"blog": "No blog found"}
