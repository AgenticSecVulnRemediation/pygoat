import pytest

# Assumption: Django app module path is introduction.views
import introduction.views as views


def test_xxe_parse_does_not_enable_external_general_entities(monkeypatch):
    # Arrange: if parser.setFeature is called with external GEs enabled, fail.
    class DummyParser:
        def setFeature(self, *args, **kwargs):
            raise AssertionError("External entity features must not be enabled")

    def fake_make_parser():
        return DummyParser()

    monkeypatch.setattr(views, "make_parser", fake_make_parser)

    def fake_parse_string(xml_str, parser=None):
        return []

    monkeypatch.setattr(views, "parseString", fake_parse_string)

    class DummyRequest:
        def __init__(self, body: bytes):
            self.body = body
            self.user = type("U", (), {"is_authenticated": True})()

    # Act
    resp = views.xxe_parse(DummyRequest(b"<root/>"))

    # Assert
    assert resp is not None
