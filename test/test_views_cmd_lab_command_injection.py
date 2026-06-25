import types

import pytest


# NOTE:
# These tests target the security changes in introduction/views.py cmd_lab:
# - domain input is validated (only [a-zA-Z0-9.-])
# - subprocess.Popen is invoked without shell=True and with argv list


def _import_views_module():
    # Import lazily so the test suite can still collect even if Django isn't configured.
    try:
        from introduction import views
        return views
    except Exception as e:
        pytest.skip(f"Unable to import introduction.views (likely missing Django settings in unit-test env): {e}")


def _fake_request(domain, os_value='linux', authenticated=True):
    user = types.SimpleNamespace(is_authenticated=authenticated)
    post = {'domain': domain, 'os': os_value}
    return types.SimpleNamespace(user=user, method='POST', POST=post)


def test_cmd_lab_rejects_invalid_domain_input():
    views = _import_views_module()

    req = _fake_request('example.com; rm -rf /', os_value='linux')

    with pytest.raises(ValueError, match='Invalid domain input'):
        views.cmd_lab(req)


def test_cmd_lab_invokes_popen_with_argv_list_and_no_shell(mocker):
    views = _import_views_module()

    # Arrange: stub render to avoid needing Django templates
    mocker.patch.object(views, 'render', side_effect=lambda request, tpl, ctx=None: {'tpl': tpl, 'ctx': ctx or {}})

    popen_mock = mocker.patch.object(views.subprocess, 'Popen', autospec=True)

    proc = mocker.Mock()
    proc.communicate.return_value = (b'OK', b'')
    popen_mock.return_value = proc

    req = _fake_request('www.Example-Domain.com', os_value='linux')

    # Act
    result = views.cmd_lab(req)

    # Assert: command must be argv list and shell must not be used
    popen_mock.assert_called_once()
    args, kwargs = popen_mock.call_args

    assert args[0] == ['dig', 'Example-Domain.com']
    assert 'shell' not in kwargs
    assert result['ctx']['output'] == 'OK'
