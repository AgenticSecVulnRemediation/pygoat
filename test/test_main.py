import os

import pytest

# Assumption: module is importable as introduction.playground.ssrf.main
from introduction.playground.ssrf import main as ssrf_main


def test_ssrf_lab_blocks_path_traversal_outside_module_dir(tmp_path, monkeypatch):
    # Arrange: make __file__ point to a controlled directory
    base_dir = tmp_path / "ssrf"
    base_dir.mkdir()
    (base_dir / "ok.txt").write_text("hello")

    monkeypatch.setattr(ssrf_main, "__file__", str(base_dir / "main.py"))

    # Act: attempt traversal to escape base_dir
    result = ssrf_main.ssrf_lab("../secret.txt")

    # Assert: traversal is blocked and generic response returned
    assert result == {"blog": "No blog found"}


def test_ssrf_lab_allows_reading_file_within_module_dir(tmp_path, monkeypatch):
    # Arrange
    base_dir = tmp_path / "ssrf"
    base_dir.mkdir()
    (base_dir / "blog.txt").write_text("blog-data")

    monkeypatch.setattr(ssrf_main, "__file__", str(base_dir / "main.py"))

    # Act
    result = ssrf_main.ssrf_lab("blog.txt")

    # Assert
    assert result == {"blog": "blog-data"}
