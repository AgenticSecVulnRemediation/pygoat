import os

import pytest

# views.py expects Django; these are narrow unit tests that patch dependencies.
import introduction.views as views


class _DummyUser:
    def __init__(self, authenticated=True):
        self.is_authenticated = authenticated


class _DummyRequest:
    def __init__(self, user, blog_value):
        self.user = user
        self.method = 'POST'
        self.POST = {'blog': blog_value}


def test_ssrf_lab_blocks_path_traversal(monkeypatch, tmp_path):
    # Arrange
    base_dir = tmp_path / 'base'
    base_dir.mkdir()

    # Make __file__ appear inside base_dir
    fake_views_file = str(base_dir / 'views.py')
    monkeypatch.setattr(views, '__file__', fake_views_file, raising=False)

    # Stub render to return context only
    monkeypatch.setattr(views, 'render', lambda request, template, context=None: context or {})

    # If open() is called for traversal, fail the test
    def _open_fail(*args, **kwargs):
        raise AssertionError('open() should not be called for traversal attempt')

    monkeypatch.setattr(views, 'open', _open_fail, raising=False)

    req = _DummyRequest(_DummyUser(True), '../secret.txt')

    # Act
    ctx = views.ssrf_lab(req)

    # Assert
    assert ctx == {"blog": "No blog found"}


def test_ssrf_lab_reads_file_within_base_dir(monkeypatch, tmp_path):
    # Arrange
    base_dir = tmp_path / 'base'
    base_dir.mkdir()
    (base_dir / 'blog.txt').write_text('hello', encoding='utf-8')

    fake_views_file = str(base_dir / 'views.py')
    monkeypatch.setattr(views, '__file__', fake_views_file, raising=False)

    monkeypatch.setattr(views, 'render', lambda request, template, context=None: context or {})

    req = _DummyRequest(_DummyUser(True), 'blog.txt')

    # Act
    ctx = views.ssrf_lab(req)

    # Assert
    assert ctx == {'blog': 'hello'}
