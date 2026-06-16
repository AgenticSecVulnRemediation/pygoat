import pytest


def _safe_yaml_parse(uploaded_file):
    """Local replica of the view behavior change: yaml.safe_load(file)."""
    import yaml

    return yaml.safe_load(uploaded_file)


def test_a9_yaml_uses_safe_load_rejects_python_object_tags():
    # Arrange: a malicious yaml tag that would be dangerous with yaml.load
    payload = b"!!python/object/apply:os.system ['echo pwned']"

    # Act / Assert
    with pytest.raises(Exception):
        _safe_yaml_parse(payload)
