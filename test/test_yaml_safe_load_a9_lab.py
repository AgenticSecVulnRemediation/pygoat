import pytest


def test_views_uses_yaml_safe_load_in_a9_lab():
    """Delta test: YAML unsafe load replaced with safe_load."""

    with open("introduction/views.py", "r", encoding="utf-8") as f:
        content = f.read()

    assert "yaml.safe_load" in content
    assert "yaml.load(file,yaml.Loader)" not in content
