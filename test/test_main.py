import os

import pytest

# Assumption: repository root is on PYTHONPATH in test runner.
from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_absolute_paths():
    resp = ssrf_lab("/etc/passwd")
    assert resp["blog"].startswith("Invalid file path")


def test_ssrf_lab_rejects_parent_traversal_paths():
    resp = ssrf_lab("../secrets.txt")
    assert resp["blog"].startswith("Invalid file path")


def test_ssrf_lab_rejects_normalized_escape_paths(mocker):
    # Force a join that escapes without containing '..' in the input, then ensure it is blocked by startswith check.
    mocker.patch("os.path.dirname", return_value="/app/ssrf")
    mocker.patch("os.path.join", return_value="/app/ssrf/ok/../../etc/passwd")
    mocker.patch("os.path.normpath", return_value="/app/etc/passwd")

    resp = ssrf_lab("ok/../../etc/passwd")
    assert resp["blog"].startswith("Invalid file path")
