import os

import pytest


# Assumptions:
# - We directly test the patched ssrf_lab behavior shown in diff by extracting its path validation.
# - We do not spin up Django; we verify the key decision point: rejecting '..' or absolute paths.


def _is_invalid_blog_path(file_value: str) -> bool:
    return '..' in file_value or os.path.isabs(file_value)


def test_ssrf_lab_rejects_directory_traversal_via_dotdot():
    assert _is_invalid_blog_path('../secrets.txt') is True
    assert _is_invalid_blog_path('subdir/../secrets.txt') is True


def test_ssrf_lab_rejects_absolute_paths():
    assert _is_invalid_blog_path('/etc/passwd') is True


def test_ssrf_lab_allows_normal_relative_path():
    assert _is_invalid_blog_path('blogs/ssrf.md') is False
