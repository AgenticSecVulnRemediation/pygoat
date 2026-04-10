import importlib


def test_a9_lab_uses_yaml_safe_load(monkeypatch):
    # Arrange
    views = importlib.import_module('introduction.views')

    called = {"safe_load": False, "load": False}

    def fake_safe_load(_file):
        called["safe_load"] = True
        return {"ok": True}

    def fake_load(*args, **kwargs):
        called["load"] = True
        raise AssertionError("yaml.load should not be used")

    monkeypatch.setattr(views.yaml, "safe_load", fake_safe_load)
    monkeypatch.setattr(views.yaml, "load", fake_load)

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        user = DummyUser()
        method = "POST"
        FILES = {"file": object()}

    # Patch render to avoid Django template rendering dependency
    def fake_render(_request, _template, context=None):
        return context

    monkeypatch.setattr(views, "render", fake_render)

    # Act
    result = views.a9_lab(DummyRequest())

    # Assert
    assert called["safe_load"] is True
    assert called["load"] is False
    assert result == {"data": {"ok": True}}
