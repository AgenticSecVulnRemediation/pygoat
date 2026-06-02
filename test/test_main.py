import os

import pytest

from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_path_traversal_attempt():
    # Previously, '../../etc/passwd' style paths could be joined and opened.
    # The fix enforces the final canonical path stays within the module directory.
    res = ssrf_lab(os.path.join('..', '..', 'etc', 'passwd'))
    assert res == {"blog": "No blog found"}


def test_ssrf_lab_allows_file_within_module_directory(tmp_path, monkeypatch):
    # Arrange: point __file__-relative dirname to a temp directory.
    base_dir = tmp_path
    (base_dir / 'blog.txt').write_text('hello')

    # Monkeypatch the module __file__ so ssrf_lab computes dirname from tmp.
    import introduction.playground.ssrf.main as ssrf_module

    monkeypatch.setattr(ssrf_module, '__file__', str(base_dir / 'main.py'))

    # Act
    res = ssrf_module.ssrf_lab('blog.txt')

    # Assert
    assert res == {"blog": "hello"}
