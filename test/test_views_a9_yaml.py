import importlib


def test_yaml_uses_safe_load(monkeypatch):
    """Regression: yaml.load(file, Loader) replaced by yaml.safe_load(file)."""

    views = importlib.import_module('introduction.views')

    class DummyUser:
        is_authenticated = True

    class DummyUploadedFile:
        pass

    class DummyRequest:
        user = DummyUser()
        method = 'POST'

        def __init__(self):
            self.FILES = {'file': DummyUploadedFile()}

    called = {'safe': 0, 'load': 0}

    def safe_load(file_obj):
        called['safe'] += 1
        return {'ok': True}

    def load(*args, **kwargs):
        called['load'] += 1
        raise AssertionError('yaml.load should not be called')

    monkeypatch.setattr(views.yaml, 'safe_load', safe_load)
    monkeypatch.setattr(views.yaml, 'load', load)

    # Patch render to avoid Django template rendering dependency; just return the context
    def fake_render(request, template, context=None):
        return context or {}

    monkeypatch.setattr(views, 'render', fake_render)

    # Act
    ctx = views.a9_lab(DummyRequest())

    # Assert
    assert called['safe'] == 1
    assert called['load'] == 0
    assert ctx['data'] == {'ok': True}
