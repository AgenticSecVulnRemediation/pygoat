import types
import pytest


# Assumption: Django app module path is introduction.views
# Tests focus only on XXE mitigation: feature_external_ges must be set to False.


def _make_request(user_authenticated=True, body=b"<root/>"):
    user = types.SimpleNamespace(is_authenticated=user_authenticated)
    return types.SimpleNamespace(user=user, body=body)


def test_xxe_parse_disables_external_general_entities(monkeypatch):
    import introduction.views as views

    request = _make_request(body=b"<root><text>hi</text></root>")

    captured = {"feature": None, "value": None}

    class DummyParser:
        def setFeature(self, feature, value):
            captured["feature"] = feature
            captured["value"] = value

    monkeypatch.setattr(views, "make_parser", lambda: DummyParser())

    class DummyDoc:
        def __iter__(self):
            return iter([])

    monkeypatch.setattr(views, "parseString", lambda *_a, **_k: DummyDoc())
    monkeypatch.setattr(views.comments.objects, "filter", lambda **_k: types.SimpleNamespace(update=lambda **_u: 1))
    monkeypatch.setattr(views, "render", lambda *_a, **_k: {"ok": True})

    views.xxe_parse(request)

    assert captured["feature"] == views.feature_external_ges
    assert captured["value"] is False
