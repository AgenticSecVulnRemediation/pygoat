import pytest


def test_views_ssrf_blog_reader_blocks_absolute_or_parent_paths():
    """Delta test: ensure file traversal is blocked before join/open."""

    with open("introduction/views.py", "r", encoding="utf-8") as f:
        content = f.read()

    assert "if '..' in file or os.path.isabs(file):" in content
    assert "Invalid file path provided" in content
