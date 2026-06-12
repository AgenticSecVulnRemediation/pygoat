import os
from pathlib import Path

import pytest

from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_path_traversal_attempt(tmp_path, monkeypatch):
    """Regression test for traversal guard added in ssrf_lab.

    Before the fix, a path like "../../secret.txt" could escape the base directory.
    After the fix, such input must not be read and should fall back to the default response.
    """
    # Arrange: sandbox the module directory so we can create an "outside" file
    sandbox_dir = tmp_path / "sandbox"
    sandbox_dir.mkdir()

    module_dir = sandbox_dir / "module"
    module_dir.mkdir()

    outside_file = sandbox_dir / "outside.txt"
    outside_file.write_text("TOP-SECRET")

    # ssrf_lab uses os.path.dirname(__file__) from its module; replace __file__ to point into module_dir
    import introduction.playground.ssrf.main as ssrf_module

    monkeypatch.setattr(ssrf_module, "__file__", str(module_dir / "main.py"))

    # Act
    result = ssrf_lab("../outside.txt")

    # Assert
    assert result == {"blog": "No blog found"}


def test_ssrf_lab_allows_reading_file_inside_module_directory(tmp_path, monkeypatch):
    """Ensure the traversal defense does not break legitimate reads within the module directory."""
    # Arrange
    module_dir = tmp_path / "module"
    module_dir.mkdir()

    blog_file = module_dir / "blog.txt"
    blog_file.write_text("hello")

    import introduction.playground.ssrf.main as ssrf_module

    monkeypatch.setattr(ssrf_module, "__file__", str(module_dir / "main.py"))

    # Act
    result = ssrf_lab("blog.txt")

    # Assert
    assert result == {"blog": "hello"}
