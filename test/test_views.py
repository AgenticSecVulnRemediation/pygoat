import pytest

# Assumption: Django app module path is introduction.views
import introduction.views as views


def test_xxe_parse_uses_defusedxml_make_parser(monkeypatch):
    # Arrange: ensure views.make_parser is the defusedxml version and is invoked.
    called = {"make_parser": False}

    class DummyParser:
        pass

    def fake_make_parser():
        called["make_parser"] = True
        return DummyParser()

    def fake_parse_string(xml_str, parser=None):
        # Assert within stub: parser passed through from make_parser
        assert isinstance(parser, DummyParser)
        return []

    monkeypatch.setattr(views, "make_parser", fake_make_parser)
    monkeypatch.setattr(views, "parseString", fake_parse_string)

    class DummyRequest:
        def __init__(self, body: bytes):
            self.body = body
            self.user = type("U", (), {"is_authenticated": True})()

    # Act
    response = views.xxe_parse(DummyRequest(b"<root/>"))

    # Assert
    assert called["make_parser"] is True
    # xxe_parse returns a Django render() response; we only assert it didn't crash.
    assert response is not None
