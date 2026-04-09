import pytest


def test_views_uses_yaml_safe_load_not_yaml_load():
    # Delta test: ensure unsafe yaml.load usage was replaced with yaml.safe_load.
    with open('introduction/views.py', 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'yaml.safe_load' in content
    assert 'yaml.load(file,yaml.Loader)' not in content
