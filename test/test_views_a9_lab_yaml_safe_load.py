import types

import pytest


# NOTE:
# Delta test for introduction/views.py a9_lab: yaml.load(..., Loader) replaced with yaml.safe_load
# We assert the view uses safe_load and does not call yaml.load.


def _import_views_module():
    try:
        from introduction import views
        return views
    except Exception as e:
        pytest.skip(f"Unable to import introduction.views (likely missing Django settings in unit-test env): {e}")


def _fake_file(name='payload.yaml', data=b'test: 1'):
    return types.SimpleNamespace(name=name, read=lambda: data)


def _fake_request(file_obj, authenticated=True):
    user = types.SimpleNamespace(is_authenticated=authenticated)
    files = {'file': file_obj}
    return types.SimpleNamespace(user=user, method='POST', FILES=files)


def test_a9_lab_uses_yaml_safe_load_not_yaml_load(mocker):
    views = _import_views_module()

    # Arrange
    mocker.patch.object(views, 'render', side_effect=lambda request, tpl, ctx=None: {'tpl': tpl, 'ctx': ctx or {}})

    safe_load = mocker.patch.object(views.yaml, 'safe_load', autospec=True, return_value={'ok': True})
    unsafe_load = mocker.patch.object(views.yaml, 'load', autospec=True, side_effect=AssertionError('yaml.load should not be called'))

    req = _fake_request(_fake_file())

    # Act
    result = views.a9_lab(req)

    # Assert
    safe_load.assert_called_once()
    assert unsafe_load.call_count == 0
    assert result['ctx']['data'] == {'ok': True}
