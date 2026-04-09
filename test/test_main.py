import os

import pytest

# Assumption: module is importable as introduction.playground.ssrf.main
from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_blocks_path_traversal_and_returns_no_blog_found(tmp_path, monkeypatch):
    # Arrange: make __file__ point to a temp directory
    fake_module_file = tmp_path / 'main.py'
    fake_module_file.write_text('# dummy')
    monkeypatch.setattr(
        __import__('introduction.playground.ssrf.main', fromlist=['__file__']),
        '__file__',
        str(fake_module_file),
        raising=False,
    )

    # Act
    result = ssrf_lab('../secrets.txt')

    # Assert
    assert result == {"blog": "No blog found"}


def test_ssrf_lab_blocks_absolute_path_and_returns_no_blog_found(tmp_path, monkeypatch):
    fake_module_file = tmp_path / 'main.py'
    fake_module_file.write_text('# dummy')
    monkeypatch.setattr(
        __import__('introduction.playground.ssrf.main', fromlist=['__file__']),
        '__file__',
        str(fake_module_file),
        raising=False,
    )

    result = ssrf_lab(os.path.abspath(str(tmp_path / 'x.txt')))

    assert result == {"blog": "No blog found"}
