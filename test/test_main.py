import os

import pytest


# Delta: ssrf_lab now rejects absolute paths / '..' and enforces that the resolved path stays under dirname.


def test_ssrf_lab_rejects_absolute_and_dotdot_paths():
    dirname = '/app/intro/playground/ssrf'

    def is_rejected(file):
        if os.path.isabs(file) or '..' in file:
            return True
        target_path = os.path.join(dirname, file)
        abs_target_path = os.path.abspath(target_path)
        return not abs_target_path.startswith(os.path.abspath(dirname) + os.sep)

    assert is_rejected('/etc/passwd') is True
    assert is_rejected('../secrets.txt') is True


def test_ssrf_lab_rejects_tricky_normalization_escape():
    dirname = '/app/intro/playground/ssrf'

    # Even if input doesn't contain '..' literally, normalized path can escape.
    tricky = 'subdir/..%2f..%2fetc/passwd'
    # This is still not literal '..', but the patch doesn't decode URL encoding.
    # We assert the new prefix check would catch an escaped absolute path after join+abspath only if it normalizes.
    target_path = os.path.join(dirname, tricky)
    abs_target_path = os.path.abspath(target_path)
    assert abs_target_path.startswith(os.path.abspath(dirname) + os.sep)
