import pytest


def test_ssrf_lab_views_uses_safe_join_and_rejects_traversal():
    """Delta test: ensure ssrf_lab view uses safe_join and blocks traversal/absolute paths."""

    with open("introduction/views.py", "r", encoding="utf-8") as f:
        content = f.read()

    assert "from django.utils._os import safe_join" in content
    assert "safe_join(dirname, file)" in content
    assert "os.path.isabs(file) or '..' in file" in content
