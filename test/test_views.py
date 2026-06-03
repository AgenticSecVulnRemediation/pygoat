import io

import introduction.views as views


class _DummyUser:
    is_authenticated = True


class _FakeFile:
    def __init__(self, data: bytes):
        self._data = data

    def read(self, *args, **kwargs):
        return self._data


class _FakeRequest:
    def __init__(self, yaml_bytes: bytes):
        self.method = "POST"
        self.user = _DummyUser()
        self.FILES = {"file": _FakeFile(yaml_bytes)}


def test_a9_lab_uses_safe_load_instead_of_yaml_load(monkeypatch):
    """Regression: ensure yaml.safe_load is used (prevents unsafe object construction)."""

    # Arrange
    def _fake_render(_request, _template, context=None, **_kwargs):
        return context

    monkeypatch.setattr(views, "render", _fake_render)

    calls = {"safe": 0, "load": 0}

    def _safe_load(file_obj):
        calls["safe"] += 1
        # minimal valid return
        return {"k": "v"}

    def _unsafe_load(*args, **kwargs):
        calls["load"] += 1
        raise AssertionError("yaml.load should not be called")

    monkeypatch.setattr(views.yaml, "safe_load", _safe_load)
    monkeypatch.setattr(views.yaml, "load", _unsafe_load)

    # Act
    ctx = views.a9_lab(_FakeRequest(b"k: v\n"))

    # Assert
    assert calls["safe"] == 1
    assert calls["load"] == 0
    assert ctx["data"] == {"k": "v"}
