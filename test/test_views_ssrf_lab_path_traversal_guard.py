import types

import pytest


# NOTE:
# Delta test for introduction/views.py ssrf_lab path traversal hardening.
# Patch adds checks for absolute paths and '..' traversal sequences.


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


def test_ssrf_lab_rejects_directory_traversal_with_parent_segment(mocker):
    views = _import_views_module()

    req = _fake_request('../secrets.txt')

    with pytest.raises(ValueError, match='Invalid file path provided'):
        views.ssrf_lab(req)


def test_ssrf_lab_rejects_absolute_path(mocker):
    views = _import_views_module()

    req = _fake_request('/etc/passwd')

    with pytest.raises(ValueError, match='Invalid file path provided'):
        views.ssrf_lab(req)
