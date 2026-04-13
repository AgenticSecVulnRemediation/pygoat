import pytest

# Assumption: module is importable as introduction.views
import introduction.views as views


def test_xxe_parse_uses_defusedxml_make_parser_and_disables_external_entities(monkeypatch):
    # Arrange
    class FakeParser:
        def __init__(self):
            self.features = []

        def setFeature(self, feature, value):
            self.features.append((feature, value))

    fake_parser = FakeParser()

    def fake_make_parser():
        return fake_parser

    # parseString is imported into module namespace; ensure our stub sees passed parser
    def fake_parse_string(xml_str, parser=None):
        assert parser is fake_parser
        # Provide minimal pulldom iterable
        class FakeNode:
            tagName = "text"

            def toxml(self):
                return "<text>ok</text>"

        return [(views.START_ELEMENT, FakeNode())]

    monkeypatch.setattr(views, "make_parser", fake_make_parser)
    monkeypatch.setattr(views, "parseString", fake_parse_string)

    class _User:
        is_authenticated = True

    class _Request:
        user = _User()
        body = b"<root/>"

    # Avoid DB update and template rendering
    class FakeFilter:
        def update(self, **kwargs):
            return 1

    monkeypatch.setattr(views.comments.objects, "filter", lambda **kwargs: FakeFilter())
    monkeypatch.setattr(views, "render", lambda request, template, ctx=None: "rendered")

    # Act
    views.xxe_parse(_Request())

    # Assert
    assert (views.feature_external_ges, False) in fake_parser.features
