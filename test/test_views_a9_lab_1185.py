import io
import types
import pytest

import introduction.views as views


def test_a9_lab_uses_yaml_safe_load(monkeypatch):
    """Regression: yaml.load -> yaml.safe_load."""

    called = {'safe': False, 'load': False}

    def _safe_load(f):
        called['safe'] = True
        return {'ok': True}

    def _load(*args, **kwargs):
        called['load'] = True
        raise AssertionError('yaml.load should not be called')

    monkeypatch.setattr(views.yaml, 'safe_load', _safe_load)
    monkeypatch.setattr(views.yaml, 'load', _load)

    class _Req:
        method = 'POST'
        user = types.SimpleNamespace(is_authenticated=True)
        FILES = {'file': io.BytesIO(b"a: 1")}

    monkeypatch.setattr(views, 'render', lambda request, template, context=None: {'template': template, 'context': context})

    resp = views.a9_lab(_Req())

    assert called['safe'] is True
    assert called['load'] is False
    assert resp['context']['data'] == {'ok': True}
