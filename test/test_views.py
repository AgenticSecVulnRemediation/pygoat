import os

import pytest

import introduction.views as views


def test_ssrf_lab_blocks_path_traversal(monkeypatch):
    # Arrange: render returns context for easy assertions
    def fake_render(_request, _template, context=None):
        return context

    monkeypatch.setattr(views, 'render', fake_render)

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        user = DummyUser()
        method = 'POST'
        POST = {'blog': '../secrets.txt'}

    # Act
    ctx = views.ssrf_lab(DummyRequest())

    # Assert
    assert 'Invalid file path' in ctx['blog']


def test_ssrf_lab_strips_to_basename_before_open(monkeypatch, tmp_path):
    # Arrange
    def fake_render(_request, _template, context=None):
        return context

    monkeypatch.setattr(views, 'render', fake_render)

    # Force module dirname to a controlled temp directory
    monkeypatch.setattr(views.os.path, 'dirname', lambda _p: str(tmp_path))

    # Create file that should be opened after basename stripping
    (tmp_path / 'good.txt').write_text('hello', encoding='utf-8')

    opened = {}
    real_open = open

    def tracking_open(path, mode='r', *args, **kwargs):
        opened['path'] = path
        return real_open(path, mode, *args, **kwargs)

    monkeypatch.setattr(views, 'open', tracking_open)

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        user = DummyUser()
        method = 'POST'
        POST = {'blog': 'nested/../good.txt'}

    # Act
    ctx = views.ssrf_lab(DummyRequest())

    # Assert: open called with basename joined to dirname
    assert os.path.basename(opened['path']) == 'good.txt'
    assert ctx['blog'] == 'hello'
