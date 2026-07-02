import pathlib


def test_views_uses_yaml_safe_load_in_a9_lab():
    """Regression test: unsafe yaml.load should not be used for user-controlled file."""
    content = pathlib.Path('introduction/views.py').read_text(encoding='utf-8')
    assert 'yaml.safe_load' in content
    assert 'yaml.load(file,yaml.Loader)' not in content
