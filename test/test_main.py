import os
import pytest

from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_directory_traversal_returns_no_blog_found():
    # The fix adds checks for '..' and absolute paths; it catches exceptions and returns a generic response.
    result = ssrf_lab('../secret.txt')
    assert result == {"blog": "No blog found"}


def test_ssrf_lab_rejects_absolute_path_returns_no_blog_found(tmp_path, monkeypatch):
    # Ensure absolute paths are rejected, regardless of whether the file exists.
    abs_path = os.path.abspath(tmp_path / 'anything.txt')
    (tmp_path / 'anything.txt').write_text('data')

    result = ssrf_lab(abs_path)
    assert result == {"blog": "No blog found"}
