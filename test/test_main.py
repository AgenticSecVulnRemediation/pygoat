import os

import pytest

from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_absolute_path():
    # Previously, absolute paths could be read. Now it should reject.
    result = ssrf_lab(os.path.abspath(__file__))
    assert 'Invalid file path' in result['blog']


def test_ssrf_lab_rejects_traversal_path():
    result = ssrf_lab(os.path.join('..', 'secrets.txt'))
    assert 'Invalid file path' in result['blog']


def test_ssrf_lab_allows_safe_relative_file(tmp_path, monkeypatch):
    # Arrange: emulate module dir and create safe file inside it
    safe_dir = tmp_path / 'module'
    safe_dir.mkdir()
    f = safe_dir / 'blog.txt'
    f.write_text('hello')

    # Patch __file__ used by ssrf_lab to point into our temp module dir
    import introduction.playground.ssrf.main as mod
    monkeypatch.setattr(mod, '__file__', str(safe_dir / 'main.py'))

    # Act
    result = mod.ssrf_lab('blog.txt')

    # Assert
    assert result == {'blog': 'hello'}
