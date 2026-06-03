import types

import pytest


def test_xxe_parse_disables_external_general_entities(monkeypatch):
    """Regression test: xxe_parse must disable external general entities (feature_external_ges=False)."""
    import introduction.views as views

    # Arrange: Fake parser capturing setFeature calls
    calls = []

    class FakeParser:
        def setFeature(self, name, value):
            calls.append((name, value))

    monkeypatch.setattr(views, "make_parser", lambda: FakeParser())

    # Avoid real XML parsing / Django ORM usage
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

    # Act
    views.xxe_parse(request)

    # Assert
    assert (views.feature_external_ges, False) in calls
