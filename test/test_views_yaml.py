import io
import pytest


def test_a9_lab_uses_yaml_safe_load(monkeypatch):
    """Delta: yaml.load(file, Loader) replaced by yaml.safe_load(file)."""
    from introduction import views

    # Arrange: ensure yaml.safe_load is invoked
    safe_load = monkeypatch.spy(views.yaml, "safe_load")

    class DummyFiles(dict):
        pass

    class DummyRequest:
        def __init__(self):
            self.method = "POST"
            self.user = type("User", (), {"is_authenticated": True})()
            self.FILES = DummyFiles({"file": io.BytesIO(b"a: 1\n")})

    # render() will try to load Django templates; stub it out and capture context
    def fake_render(_req, _tmpl, context=None):
        return context

    monkeypatch.setattr(views, "render", fake_render)

    # Act
    ctx = views.a9_lab(DummyRequest())

    # Assert
    assert safe_load.call_count == 1
    assert ctx["data"] == {"a": 1}
