# Assumption: Django app module is named `introduction`.
# This test focuses only on the changed behavior: external entities are disabled.

import types


def test_xxe_parse_disables_external_entities(monkeypatch):
    import introduction.views as views

    # Arrange: record the feature flags set on parser
    class DummyParser:
        def __init__(self):
            self.features = {}

        def setFeature(self, feature, value):
            self.features[feature] = value

    dummy_parser = DummyParser()

    def _make_parser():
        return dummy_parser

    monkeypatch.setattr(views, "make_parser", _make_parser)

    # prevent actual XML parsing / DB actions
    def _parse_string(xml, parser=None):
        # ensure the parser used is the dummy and contains the security setting
        assert parser is dummy_parser
        return []

    monkeypatch.setattr(views, "parseString", _parse_string)
    monkeypatch.setattr(views, "render", lambda request, tpl: (tpl, 200))

    # mock comments ORM usage
    class DummyQS:
        def filter(self, **kwargs):
            return self

        def update(self, **kwargs):
            return 1

    monkeypatch.setattr(views, "comments", DummyQS())

    class DummyReq:
        body = b"<root><text>hi</text></root>"

    # Act
    views.xxe_parse(DummyReq())

    # Assert
    assert views.feature_external_ges in dummy_parser.features
    assert dummy_parser.features[views.feature_external_ges] is False
