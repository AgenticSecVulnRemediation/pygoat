import io

import pytest


def test_a9_lab_uses_yaml_safe_load_for_uploaded_file(monkeypatch):
    """Delta test: yaml.load(file, yaml.Loader) replaced by yaml.safe_load(file)."""
    import introduction.views as views

    called = {'safe_load': False}

    def _safe_load(f):
        called['safe_load'] = True
        # Simulate parsed content
        return {'k': 'v'}

    # If yaml.load is ever called, fail the test
    def _load(*args, **kwargs):
        raise AssertionError('yaml.load should not be called')

    monkeypatch.setattr(views.yaml, 'safe_load', _safe_load)
    monkeypatch.setattr(views.yaml, 'load', _load)

    class _DummyUser:
        is_authenticated = True

    class _DummyReq:
        method = 'POST'
        user = _DummyUser()
        FILES = {'file': io.BytesIO(b'k: v\n')}

    # Act
    resp = views.a9_lab(_DummyReq())

    # Assert
    assert called['safe_load'] is True
    assert getattr(resp, 'status_code', None) == 200
