import io

import pytest

import introduction.views as views


def test_a9_lab_uses_safe_load(monkeypatch):
    # Arrange: if unsafe yaml.load is used, fail the test
    def fail_load(*args, **kwargs):
        raise AssertionError('yaml.load should not be called; safe_load must be used')

    monkeypatch.setattr(views.yaml, 'load', fail_load)

    called = {}

    def fake_safe_load(stream):
        called['stream_type'] = type(stream)
        return {'ok': True}

    monkeypatch.setattr(views.yaml, 'safe_load', fake_safe_load)

    # Avoid rendering/template dependencies; return the context for assertion
    def fake_render(_request, _template, context=None):
        return context

    monkeypatch.setattr(views, 'render', fake_render)

    class DummyRequest:
        user = type('U', (), {'is_authenticated': True})()
        method = 'POST'

        def __init__(self):
            self.FILES = {'file': io.BytesIO(b'a: 1')}

    req = DummyRequest()

    # Act
    ctx = views.a9_lab(req)

    # Assert
    assert called['stream_type'] is io.BytesIO
    assert ctx['data'] == {'ok': True}
