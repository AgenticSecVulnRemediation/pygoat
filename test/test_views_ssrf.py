import os

import pytest


def test_ssrf_lab_rejects_absolute_path_returns_invalid_file_path(monkeypatch):
    import introduction.views as views

    class _DummyUser:
        is_authenticated = True

    class _DummyPost:
        def __init__(self, blog):
            self._blog = blog

        def __getitem__(self, key):
            if key == 'blog':
                return self._blog
            raise KeyError(key)

    class _DummyReq:
        method = 'POST'
        user = _DummyUser()

        def __init__(self, blog):
            self.POST = _DummyPost(blog)

    # Act
    resp = views.ssrf_lab(_DummyReq('/etc/passwd'))

    # Assert
    assert getattr(resp, 'status_code', None) == 200
    assert 'Invalid file path' in resp.content.decode('utf-8')


def test_ssrf_lab_rejects_traversal_outside_base_dir(monkeypatch):
    import introduction.views as views

    class _DummyUser:
        is_authenticated = True

    class _DummyPost:
        def __init__(self, blog):
            self._blog = blog

        def __getitem__(self, key):
            if key == 'blog':
                return self._blog
            raise KeyError(key)

    class _DummyReq:
        method = 'POST'
        user = _DummyUser()

        def __init__(self, blog):
            self.POST = _DummyPost(blog)

    # '../' should be blocked by commonpath check
    resp = views.ssrf_lab(_DummyReq('../secrets.txt'))
    assert 'Invalid file path' in resp.content.decode('utf-8')
