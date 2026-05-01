import os

import pytest


def test_ssrf_lab_blocks_directory_traversal_and_out_of_dir_access(mocker, tmp_path):
    """Regression: ssrf_lab() should reject abs paths / '..' and resolved paths outside dirname."""
    from introduction.playground.ssrf import main

    # Arrange
    # Ensure open() is never called for traversal attempts.
    open_spy = mocker.patch("builtins.open", autospec=True)

    # Absolute path
    assert main.ssrf_lab("/etc/passwd") == {"blog": "No blog found"}
    open_spy.assert_not_called()

    open_spy.reset_mock()

    # Parent traversal
    assert main.ssrf_lab("../secret.txt") == {"blog": "No blog found"}
    open_spy.assert_not_called()

    open_spy.reset_mock()

    # Path that resolves outside directory via join trick
    # Using leading separator makes it absolute on *nix; already covered. Use '..' path is covered.
