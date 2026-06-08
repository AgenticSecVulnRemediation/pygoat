import json

import pytest


# Assumption: module path is introduction.playground.ssrf.main as indicated by file_path.
from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_absolute_path():
    assert ssrf_lab("/etc/passwd") == {"blog": "Invalid file path provided"}


def test_ssrf_lab_rejects_parent_directory_traversal():
    assert ssrf_lab("../secrets.txt") == {"blog": "Invalid file path provided"}


def test_ssrf_lab_rejects_nested_parent_directory_traversal():
    assert ssrf_lab("posts/../../secrets.txt") == {"blog": "Invalid file path provided"}
