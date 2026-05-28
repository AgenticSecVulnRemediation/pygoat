import os
import pytest


def test_xxe_parse_disables_external_entities(monkeypatch):
    """Regression for XXE fix: feature_external_ges must be set to False."""
    from introduction import views

    class FakeParser:
        def __init__(self):
            self.features = {}

        def setFeature(self, feature, value):
            self.features[feature] = value

    fake_parser = FakeParser()

    def fake_make_parser():
        return fake_parser

    # Avoid actually parsing XML
    def fake_parse_string(_body, parser=None):
        assert parser is fake_parser
        return []

    class DummyRequest:
        user = type('U', (), {'is_authenticated': True})()
        body = b"<root/>"

    monkeypatch.setattr(views, "make_parser", fake_make_parser)
    monkeypatch.setattr(views, "parseString", fake_parse_string)

    # Stub render
    monkeypatch.setattr(views, "render", lambda *_args, **_kwargs: {})

    views.xxe_parse(DummyRequest())

    assert views.feature_external_ges in fake_parser.features
    assert fake_parser.features[views.feature_external_ges] is False
