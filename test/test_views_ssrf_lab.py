import os

import pytest


# Tests cover the SSRF/path traversal hardening in ssrf_lab (introduction/views.py):
# user-controlled filename is replaced by allow-list selection.


def test_ssrf_lab_invalid_blog_selection_does_not_open_file(mocker):
    from introduction import views

    open_mock = mocker.patch('builtins.open', side_effect=AssertionError("open must not be called"))

    class _Req:
        user = mocker.Mock(is_authenticated=True)
        method = "POST"
        POST = {'blog': '../../etc/passwd'}

    resp = views.ssrf_lab(_Req())

    # We can't easily inspect template context without Django test client;
    # assert the secure behavior: file open was not attempted.
    assert not open_mock.called
    assert resp is not None


def test_ssrf_lab_valid_blog_selection_uses_allow_list_file(mocker, tmp_path):
    from introduction import views

    # Ensure os.path.join is used with the allow-listed filename 'blog.txt'
    join_spy = mocker.spy(os.path, 'join')

    # Patch dirname and open to return deterministic content.
    mocker.patch('introduction.views.os.path.dirname', return_value=str(tmp_path))
    blog_path = tmp_path / 'blog.txt'
    blog_path.write_text('hello')

    class _Req:
        user = mocker.Mock(is_authenticated=True)
        method = "POST"
        POST = {'blog': 'blog'}

    resp = views.ssrf_lab(_Req())

    assert any('blog.txt' in str(call.args[1]) for call in join_spy.mock_calls)
    assert resp is not None
