import types


def test_a9_lab_uses_yaml_safe_load(monkeypatch):
    """Delta test: introduction.views.a9_lab now uses yaml.safe_load instead of yaml.load.

    We assert safe_load is invoked and yaml.load is not.
    """

    import introduction.views as views

    called = {"safe_load": 0, "load": 0}

    def fake_safe_load(file_obj):
        called["safe_load"] += 1
        return {"ok": True}

    def fake_load(*args, **kwargs):
        called["load"] += 1
        raise AssertionError("yaml.load should not be used")

    monkeypatch.setattr(views.yaml, "safe_load", fake_safe_load)
    monkeypatch.setattr(views.yaml, "load", fake_load)

    class DummyFiles(dict):
        pass

    class DummyRequest:
        def __init__(self):
            self.user = types.SimpleNamespace(is_authenticated=True)
            self.method = "POST"
            self.FILES = DummyFiles(file=object())

    # render returns context for inspection
    monkeypatch.setattr(views, "render", lambda request, template, context=None: context)

    ctx = views.a9_lab(DummyRequest())

    assert called["safe_load"] == 1
    assert called["load"] == 0
    assert ctx["data"] == {"ok": True}
