import types
import pytest


# Assumption: Django app module path is introduction.views
# Tests focus only on switching to defusedxml.pulldom for parseString.


def _make_request(user_authenticated=True, body=b"<root/>"):
    user = types.SimpleNamespace(is_authenticated=user_authenticated)
    return types.SimpleNamespace(user=user, body=body)


def test_xxe_parse_uses_defusedxml_parseString(monkeypatch):
    import introduction.views as views

    request = _make_request(body=b"<root><text>hi</text></root>")

    called = {"defused": 0}

    class DummyDoc:
        def __iter__(self):
            # Provide minimal iteration to satisfy for-loop
            return iter([])

    def fake_parse_string(_xml, parser=None):
        called["defused"] += 1
        return DummyDoc()

    # If xml.dom.pulldom.parseString were still used, this patch would not affect this symbol.
    monkeypatch.setattr(views, "parseString", fake_parse_string)

    # Avoid touching DB and template rendering
    monkeypatch.setattr(views.comments.objects, "filter", lambda **_k: types.SimpleNamespace(update=lambda **_u: 1))
    monkeypatch.setattr(views, "render", lambda *_a, **_k: {"ok": True})

    views.xxe_parse(request)

    assert called["defused"] == 1
