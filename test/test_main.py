import os
from unittest.mock import mock_open

import pytest


# Assumptions:
# - Function under test is `introduction.playground.ssrf.main.ssrf_lab`.


def test_ssrf_lab_rejects_dotdot_path_traversal(monkeypatch):
    from introduction.playground.ssrf import main

    # Ensure open() is never called for traversal attempts.
    open_spy = mock_open(read_data="secret")
    monkeypatch.setattr(main, "open", open_spy, raising=False)

    result = main.ssrf_lab("../secrets.txt")

    assert result == {"blog": "No blog found"}
    open_spy.assert_not_called()


def test_ssrf_lab_rejects_absolute_path(monkeypatch):
    from introduction.playground.ssrf import main

    open_spy = mock_open(read_data="secret")
    monkeypatch.setattr(main, "open", open_spy, raising=False)

    result = main.ssrf_lab(os.path.abspath("/etc/passwd"))

    assert result == {"blog": "No blog found"}
    open_spy.assert_not_called()
