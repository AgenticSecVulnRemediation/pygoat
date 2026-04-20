import os

import pytest

# Assumption: ssrf_lab is importable from introduction.playground.ssrf.main
from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_absolute_path():
    assert ssrf_lab("/etc/passwd") == {"blog": "No blog found"}


def test_ssrf_lab_rejects_dotdot_path_traversal():
    assert ssrf_lab("../secrets.txt") == {"blog": "No blog found"}
