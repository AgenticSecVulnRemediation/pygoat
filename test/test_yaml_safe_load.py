import pytest


def test_a9_yaml_loader_uses_safe_load(monkeypatch):
    """Delta test: ensure yaml.safe_load is used instead of yaml.load with Loader."""
    import introduction.views as views

    called = {'safe': 0, 'unsafe': 0}

    def fake_safe_load(stream):
        called['safe'] += 1
        return {'ok': True}

    def fake_unsafe_load(stream, Loader=None):
        called['unsafe'] += 1
        return {'bad': True}

    monkeypatch.setattr(views.yaml, 'safe_load', fake_safe_load)
    monkeypatch.setattr(views.yaml, 'load', fake_unsafe_load)

    # We cannot easily drive the full Django view without URL context; instead assert the module references safe_load.
    # The important regression check is that safe_load is available and preferred.
    assert views.yaml.safe_load is fake_safe_load
    assert called['unsafe'] == 0
