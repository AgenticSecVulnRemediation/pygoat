import yaml


def test_a9_lab_uses_yaml_safe_load():
    """Regression test: YAML parsing must use safe_load (no arbitrary object construction)."""
    with open('introduction/views.py', 'r', encoding='utf-8') as f:
        src = f.read()

    assert 'yaml.safe_load' in src
    assert 'yaml.load(file,yaml.Loader)' not in src.replace(' ', '')
