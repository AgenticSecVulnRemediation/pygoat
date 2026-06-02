import os

import pytest

from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_absolute_path():
    # Absolute paths must be rejected to prevent reading arbitrary files
    assert ssrf_lab('/etc/passwd') == {"blog": "No blog found"}


def test_ssrf_lab_rejects_directory_traversal_path():
    # Directory traversal must be rejected
    assert ssrf_lab('../secrets.txt') == {"blog": "No blog found"}
