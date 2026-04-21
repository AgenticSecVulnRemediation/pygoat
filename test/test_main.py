import os
import pytest

# Assumption: tests run with project root on PYTHONPATH so `introduction` is importable.
from introduction.playground.ssrf import main


def test_ssrf_lab_blocks_directory_traversal_and_never_opens_file(mocker):
    open_spy = mocker.patch("builtins.open", autospec=True)

    result = main.ssrf_lab("../secrets.txt")

    assert result == {"blog": "No blog found"}
    open_spy.assert_not_called()


def test_ssrf_lab_blocks_absolute_path_and_never_opens_file(mocker):
    open_spy = mocker.patch("builtins.open", autospec=True)

    result = main.ssrf_lab(os.path.abspath("/etc/passwd"))

    assert result == {"blog": "No blog found"}
    open_spy.assert_not_called()
