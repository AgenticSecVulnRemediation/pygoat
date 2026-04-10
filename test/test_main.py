import os

import pytest

from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_absolute_path_and_dotdot_traversal():
    # Absolute path should be rejected
    assert ssrf_lab('/etc/passwd') == {"blog": "Invalid file path"}

    # Directory traversal should be rejected
    assert ssrf_lab('../secrets.txt') == {"blog": "Invalid file path"}
