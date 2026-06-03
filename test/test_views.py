import pytest


def _load_yaml_securely(file_obj):
    """Mirror the patched behavior: use yaml.safe_load (no Loader argument)."""
    import yaml

    return yaml.safe_load(file_obj)


def test_yaml_safe_load_rejects_python_object_tags():
    # This is a common exploit vector against yaml.load(..., Loader=...)
    payload = "!!python/object/apply:os.system ['echo pwned']"

    # safe_load should not construct arbitrary Python objects.
    with pytest.raises(Exception):
        _load_yaml_securely(payload)
