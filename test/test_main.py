import os
import pytest

# Assumption: module can be imported using repo-relative package path
from introduction.playground.ssrf import main


def test_ssrf_lab_rejects_absolute_path_before_try_block():
    with pytest.raises(ValueError, match='Invalid file path provided'):
        main.ssrf_lab('/etc/passwd')


def test_ssrf_lab_rejects_parent_traversal_before_try_block():
    with pytest.raises(ValueError, match='Invalid file path provided'):
        main.ssrf_lab('../secrets.txt')
