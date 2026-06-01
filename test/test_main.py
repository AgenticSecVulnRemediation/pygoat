import os
import tempfile

from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_blocks_directory_traversal_relative_parent(tmp_path):
    """Delta: ssrf_lab now rejects '..' / normpath escape attempts and returns the safe fallback."""
    # Act
    res = ssrf_lab("../secrets.txt")

    # Assert
    assert res == {"blog": "No blog found"}


def test_ssrf_lab_allows_normalized_safe_relative_path(tmp_path, monkeypatch):
    """Delta: ssrf_lab normalizes safe paths and still reads within the module directory."""
    # Arrange: create a temp module directory with a file and monkeypatch __file__ dirname resolution
    module_dir = tmp_path / "mod"
    module_dir.mkdir()
    blog_file = module_dir / "blog.txt"
    blog_file.write_text("hello")

    # ssrf_lab uses os.path.dirname(__file__)
    monkeypatch.setattr("introduction.playground.ssrf.main.__file__", str(module_dir / "main.py"))

    # Act
    res = ssrf_lab("./blog.txt")

    # Assert
    assert res == {"blog": "hello"}
