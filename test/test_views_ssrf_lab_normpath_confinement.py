import types

import pytest


# NOTE:
# Delta test for introduction/views.py ssrf_lab hardening:
# - reject abs paths and '..'
# - reject paths that escape base dir after normpath
# We assert that a traversal attempt returns an "Invalid file path" response.


def _import_views_module():
    try:
        from introduction import views
        return views
    except Exception as e:
        pytest.skip(f"Unable to import introduction.views (likely missing Django settings in unit-test env): {e}")


def _fake_request(blog_value: str, authenticated=True):
    user = types.SimpleNamespace(is_authenticated=authenticated)
    post = {'blog': blog_value}
    return types.SimpleNamespace(user=user, method='POST', POST=post)


def test_ssrf_lab_returns_invalid_file_path_for_traversal_attempt(mocker):
    views = _import_views_module()

    # Arrange: stub render so we can observe the context
    mocker.patch.object(views, 'render', side_effect=lambda request, tpl, ctx=None: {'tpl': tpl, 'ctx': ctx or {}})

    # Force join to produce a path that will fail the normpath/startswith check.
    mocker.patch.object(views.os.path, 'isabs', return_value=False)
    mocker.patch.object(views.os.path, 'dirname', return_value='/base/dir')
    mocker.patch.object(views.os.path, 'join', return_value='/base/dir/../escape.txt')

    # After normalization it escapes base dir
    mocker.patch.object(views.os.path, 'normpath', return_value='/base/escape.txt')

    req = _fake_request('ok.txt')

    # Act
    result = views.ssrf_lab(req)

    # Assert
    assert result['ctx']['blog'] == 'Invalid file path'
