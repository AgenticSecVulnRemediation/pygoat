import pytest


# Delta covered: ssrf_lab now rejects absolute paths and traversal ('..').

def test_ssrf_lab_rejects_traversal_and_abs_path(mocker):
    from introduction.playground.ssrf import main

    open_mock = mocker.patch("builtins.open", side_effect=AssertionError("open() must not be called"))

    assert main.ssrf_lab("../secret.txt") == {"blog": "No blog found"}
    assert open_mock.call_count == 0

    assert main.ssrf_lab("/etc/passwd") == {"blog": "No blog found"}
    assert open_mock.call_count == 0
