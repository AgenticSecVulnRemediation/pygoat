import os

import pytest


# Assumption: module import path is "introduction.playground.ssrf.main" based on repository structure.
from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_path_traversal_returns_no_blog_found(tmp_path, monkeypatch):
    """Regression for path traversal: attempts to escape base_dir must be blocked."""
    # Arrange: force base_dir used by ssrf_lab to a temp directory
    base_dir = tmp_path / "base"
    base_dir.mkdir()

    realpath_original = os.path.realpath

    def fake_realpath(p):
        # os.path.realpath(__file__) should resolve to a file under base_dir
        if p == __file__:
            return str(base_dir / "main.py")
        return realpath_original(p)

    monkeypatch.setattr(os.path, "realpath", fake_realpath)

    # Act: attempt to traverse outside base_dir
    result = ssrf_lab("../secrets.txt")

    # Assert
    assert result == {"blog": "No blog found"}


def test_ssrf_lab_valid_relative_path_reads_file(tmp_path, monkeypatch):
    """Valid relative paths under base_dir are still allowed."""
    base_dir = tmp_path / "base"
    base_dir.mkdir()
    (base_dir / "blog.txt").write_text("hello", encoding="utf-8")

    realpath_original = os.path.realpath

    def fake_realpath(p):
        if p == __file__:
            return str(base_dir / "main.py")
        return realpath_original(p)

    monkeypatch.setattr(os.path, "realpath", fake_realpath)

    result = ssrf_lab("blog.txt")

    assert result == {"blog": "hello"}
