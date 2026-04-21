import types

import pytest

# Assumption: module path is importable as introduction.views
from introduction import views


def _make_request(body: bytes):
    user = types.SimpleNamespace(is_authenticated=True)
    req = types.SimpleNamespace()
    req.user = user
    req.body = body
    return req


def test_xxe_parse_disables_external_ges(monkeypatch):
    # Arrange
    seen = {}

    class FakeParser:
        def setFeature(self, feature, value):
            seen["feature"] = feature
            seen["value"] = value

    def fake_make_parser():
        return FakeParser()

    # parseString is called with parser kwarg
    def fake_parse_string(xml, parser=None):
        assert isinstance(parser, FakeParser)
        # Minimal pulldom-like iterable
        class FakeDoc:
            def __iter__(self_inner):
                return iter([])

        return FakeDoc()

    monkeypatch.setattr(views, "make_parser", fake_make_parser)
    monkeypatch.setattr(views, "parseString", fake_parse_string)

    # Act
    views.xxe_parse(_make_request(b"<root></root>"))

    # Assert
    assert seen["feature"] == views.feature_external_ges
    assert seen["value"] is False
