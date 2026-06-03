import os

import pytest

from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_absolute_path():
    # Previously, absolute paths could be passed through to open(); now they must be rejected.
    with pytest.raises(ValueError, match="Absolute paths"):
        ssrf_lab("/etc/passwd")


def test_ssrf_lab_rejects_parent_directory_traversal():
    # Previously, traversal sequences could escape the intended directory.
    with pytest.raises(ValueError, match="directory traversal"):
        ssrf_lab("../secrets.txt")
