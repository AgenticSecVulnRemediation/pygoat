import pytest

from introduction.playground.ssrf import main


def test_ssrf_lab_blocks_absolute_paths(mocker):
    open_spy = mocker.patch("builtins.open", side_effect=AssertionError("open should not be called"))

    resp = main.ssrf_lab("/etc/passwd")

    assert resp == {"blog": "No blog found"}
    open_spy.assert_not_called()


def test_ssrf_lab_blocks_parent_traversal_paths(mocker):
    open_spy = mocker.patch("builtins.open", side_effect=AssertionError("open should not be called"))

    resp = main.ssrf_lab("../secrets.txt")

    assert resp == {"blog": "No blog found"}
    open_spy.assert_not_called()
