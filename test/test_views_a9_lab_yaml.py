import io

import pytest


def test_a9_lab_uses_yaml_safe_load(monkeypatch):
    # Regression test: ensure yaml.safe_load is used instead of yaml.load(..., Loader).
    from introduction import views

    called = {'safe': False}

    def fake_safe_load(_file):
        called['safe'] = True
        return {'ok': True}

    monkeypatch.setattr(views.yaml, 'safe_load', fake_safe_load)

    # If yaml.load is still used, this will raise and fail the test.
    def fail_load(*args, **kwargs):
        raise AssertionError('yaml.load should not be used')

    monkeypatch.setattr(views.yaml, 'load', fail_load)

    class Req:
        user = type('U', (), {'is_authenticated': True})()
        method = 'POST'
        FILES = {'file': io.BytesIO(b'key: value')}

    views.a9_lab(Req())

    assert called['safe'] is True
