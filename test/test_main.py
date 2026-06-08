import os

import pytest

from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_absolute_path():
    # absolute paths must be rejected to prevent traversal
    with pytest.raises(ValueError):
        ssrf_lab("/etc/passwd")


def test_ssrf_lab_rejects_parent_traversal_segment():
    # parent traversal segments must be rejected
    with pytest.raises(ValueError):
        ssrf_lab("../secrets.txt")
