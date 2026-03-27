import io
import types
import pytest
import yaml

# Assumptions:
# - Django is available and introduction.views can be imported.
# - We unit-test the changed behavior by asserting yaml.safe_load is used (not yaml.load).


def test_a9_lab_uses_yaml_safe_load(mocker):
    # Arrange
    import introduction.views as views

    request = types.SimpleNamespace()
    request.user = types.SimpleNamespace(is_authenticated=True)
    request.method = "POST"
    request.FILES = {"file": io.BytesIO(b"key: value")}
    request.POST = {}

    safe_load_spy = mocker.spy(views.yaml, "safe_load")
    load_spy = mocker.spy(views.yaml, "load")

    mocker.patch.object(views, "render", return_value="RENDERED")

    # Act
    views.a9_lab(request)

    # Assert
    assert safe_load_spy.call_count == 1
    assert load_spy.call_count == 0
