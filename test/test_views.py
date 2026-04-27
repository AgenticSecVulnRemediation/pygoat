import pytest

# Assumption: this is a Django app named "introduction" and tests can import the views module.
from introduction import views


def test_a9_lab_uses_yaml_safe_load(mocker):
    # Arrange: create a fake request-like object with FILES and authenticated user
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = 'POST'
    request.FILES = {'file': mocker.Mock()}

    safe_load = mocker.patch.object(views.yaml, 'safe_load', return_value={'ok': True})
    # Guard: old vulnerable API should not be called by this codepath
    load = mocker.patch.object(views.yaml, 'load', side_effect=AssertionError('yaml.load must not be used'))

    mocker.patch.object(views, 'render', return_value='rendered')

    # Act
    resp = views.a9_lab(request)

    # Assert
    assert resp == 'rendered'
    safe_load.assert_called_once_with(request.FILES['file'])
    assert load.call_count == 0
