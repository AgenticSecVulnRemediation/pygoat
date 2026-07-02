import types

import pytest


def test_xxe_parse_does_not_enable_external_entities(monkeypatch):
    """Delta test: patched code must NOT call parser.setFeature(feature_external_ges, True)."""

    # Arrange: create a fake parser that would raise if setFeature is called.
    class FakeParser:
        def setFeature(self, *args, **kwargs):
            raise AssertionError('setFeature should not be called when using defusedxml')

    def fake_make_parser():
        return FakeParser()

    # Monkeypatch the module under test to use our fake parser
    import importlib
    views = importlib.import_module('introduction.views')

    monkeypatch.setattr(views, 'make_parser', fake_make_parser)

    # Also stub parseString/START_ELEMENT to avoid real XML parsing.
    def fake_parseString(xml, parser=None):
        assert parser is not None
        # minimal iterable matching expected loop
        class Node:
            tagName = 'text'
            def toxml(self):
                return '<text>ok</text>'
        return [(views.START_ELEMENT, Node())]

    monkeypatch.setattr(views, 'parseString', fake_parseString)

    # Stub comments ORM chain
    class FakeComments:
        class objects:
            @staticmethod
            def filter(id=None):
                class Q:
                    @staticmethod
                    def update(comment=None):
                        return 1
                return Q()

    monkeypatch.setattr(views, 'comments', FakeComments)

    class Req:
        body = b'<text>ignored</text>'
        user = types.SimpleNamespace(is_authenticated=True)

    # Act
    resp = views.xxe_parse(Req())

    # Assert: if setFeature called, test would fail.
    assert resp is not None
