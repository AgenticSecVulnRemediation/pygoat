import pytest


def test_a9_lab_uses_yaml_safe_load():
    """Regression test for unsafe YAML deserialization fix."""
    from pathlib import Path

    content = Path('introduction/views.py').read_text(encoding='utf-8')

    assert 'yaml.safe_load' in content
    assert 'yaml.load(file,yaml.Loader)' not in content
