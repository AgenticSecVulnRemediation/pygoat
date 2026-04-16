import pytest

# Assumption: repository root is on PYTHONPATH in test runner.
from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_absolute_paths():
    resp = ssrf_lab("/etc/passwd")
    assert resp["blog"].startswith("Invalid file path")


def test_ssrf_lab_rejects_parent_traversal_paths():
    resp = ssrf_lab("../secrets.txt")
    assert resp["blog"].startswith("Invalid file path")
