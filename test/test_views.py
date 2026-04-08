import types
import pytest


# Assumption: Django app module path is introduction.views
# Tests focus only on switching make_parser import to defusedxml.sax.make_parser.


def _make_request(user_authenticated=True, body=b"<root/>"):
    user = types.SimpleNamespace(is_authenticated=user_authenticated)
    return types.SimpleNamespace(user=user, body=body)


def test_xxe_parse_uses_defusedxml_make_parser(monkeypatch):
    import introduction.views as views

    request = _make_request(body=b"<root><text>hi</text></root>")

    called = {"make_parser": 0}

    class DummyParser:
        def setFeature(self, *_a, **_k):
            return None

    def fake_make_parser():
        called["make_parser"] += 1
        return DummyParser()

    class DummyDoc:
        def __iter__(self):
            return iter([])

    monkeypatch.setattr(views, "make_parser", fake_make_parser)
    monkeypatch.setattr(views, "parseString", lambda *_a, **_k: DummyDoc())
    monkeypatch.setattr(views.comments.objects, "filter", lambda **_k: types.SimpleNamespace(update=lambda **_u: 1))
    monkeypatch.setattr(views, "render", lambda *_a, **_k: {"ok": True})

    views.xxe_parse(request)

    assert called["make_parser"] == 1
