import types

import pytest


def test_views_xxe_parse_sets_external_general_entities_false(monkeypatch):
    """Regression test: with defusedxml parser, external-general-entities must be disabled."""
    import introduction.views as views

    calls = []

    class FakeParser:
        def setFeature(self, name, value):
            calls.append((name, value))

    monkeypatch.setattr(views, "make_parser", lambda: FakeParser())
    monkeypatch.setattr(views, "parseString", lambda *args, **kwargs: [])

    class DummyQuery:
        def update(self, **kwargs):
            return 1

    class DummyComments:
        class objects:
            @staticmethod
            def filter(id):
                return DummyQuery()

    monkeypatch.setattr(views, "comments", DummyComments)

    request = types.SimpleNamespace(body=b"<root></root>", user=types.SimpleNamespace(is_authenticated=True))

    views.xxe_parse(request)

    assert ('http://xml.org/sax/features/external-general-entities', False) in calls
