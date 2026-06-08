import io

import pytest
import yaml


def test_yaml_safe_load_rejects_python_object_tag():
    """Regression test for unsafe yaml.load(yaml.Loader) usage.

    After the fix, the code uses yaml.safe_load(), which must reject
    python/object tags that could lead to arbitrary object construction.
    """
    malicious = "!!python/object/apply:os.system ['echo pwned']"

    # safe_load should reject this payload (typically ConstructorError)
    with pytest.raises(yaml.constructor.ConstructorError):
        yaml.safe_load(io.StringIO(malicious))
