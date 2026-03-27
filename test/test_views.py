import io
import types
import pytest

# Assumptions:
# - Django is available and introduction.views can be imported.
# - We unit-test the changed behavior by asserting yaml.safe_load is used (not yaml.load).


def test_a9_lab_uses_yaml_safe_load_with_comment(mocker):
    # Arrange
    import introduction.views as views