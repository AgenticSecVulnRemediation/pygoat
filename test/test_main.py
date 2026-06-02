# Assumptions:
# - The project uses pytest.
# - introduction.playground.ssrf.main exposes ssrf_lab(file) for reading a local file.

import os

import pytest

from introduction.playground.ssrf import main


def test_ssrf_lab_rejects_parent_traversal_and_absolute_paths(tmp_path, monkeypatch):
    """Regression test for path traversal protection.

    The fix rejects '..' segments and absolute paths.
    The function should return the safe fallback response.
    """

    # Make __file__ directory deterministic.
    fake_module_dir = tmp_path / "mod"
    fake_module_dir.mkdir()
    monkeypatch.setattr(main, "__file__", str(fake_module_dir / "main.py"))

    # Ensure even if open is called, the test would fail.
    def _boom(*args, **kwargs):
        raise AssertionError("open() must not be reached for invalid paths")

    monkeypatch.setattr(main, "open", _boom, raising=False)

    assert main.ssrf_lab("../secrets.txt") == {"blog": "No blog found"}
    assert main.ssrf_lab(str(tmp_path / "secrets.txt")) == {"blog": "No blog found"}


def test_ssrf_lab_allows_relative_file_inside_module_dir(tmp_path, monkeypatch):
    """Sanity check: a normal relative path can still be read."""

    fake_module_dir = tmp_path / "mod"
    fake_module_dir.mkdir()
    (fake_module_dir / "blog.txt").write_text("hello")
    monkeypatch.setattr(main, "__file__", str(fake_module_dir / "main.py"))

    assert main.ssrf_lab("blog.txt") == {"blog": "hello"}
