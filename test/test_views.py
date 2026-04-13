import pytest

# Assumption: module is importable as introduction.views
import introduction.views as views


def test_xxe_parse_disables_external_entities_feature(monkeypatch):
    class FakeParser:
        def __init__(self):
            self.features = []

        def setFeature(self, feature, value):
            self.features.append((feature, value))

    fake_parser = FakeParser()

    monkeypatch.setattr(views, "make_parser", lambda: fake_parser)

    def fake_parse_string(xml_str, parser=None):
        assert parser is fake_parser

        class FakeNode:
            tagName = "text"

            def toxml(self):
                return "<text>ok</text>"

        return [(views.START_ELEMENT, FakeNode())]

    monkeypatch.setattr(views, "parseString", fake_parse_string)

    class _User:
        is_authenticated = True

    class _Request:
        user = _User()
        body = b"<root/>"

    class FakeFilter:
        def update(self, **kwargs):
            return 1

    monkeypatch.setattr(views.comments.objects, "filter", lambda **kwargs: FakeFilter())
    monkeypatch.setattr(views, "render", lambda request, template, ctx=None: "rendered")

    views.xxe_parse(_Request())

    assert (views.feature_external_ges, False) in fake_parser.features
