import os
import pytest

from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_blocks_directory_traversal(tmp_path, monkeypatch):
    # Arrange: attempt to traverse outside the module directory
    result = ssrf_lab("../../etc/passwd")

    # Assert: should not return file contents
    assert result == {"blog": "No blog found"}
