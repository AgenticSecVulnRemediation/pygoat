import introduction.views as views


def test_xxe_parse_no_longer_enables_external_general_entities(monkeypatch):
    # The fix removed the explicit call:
    #   parser.setFeature(feature_external_ges, True)
    # Assert that xxe_parse does not call setFeature at all.

    class FakeParser:
        def __init__(self):
            self.set_feature_calls = []

        def setFeature(self, *args, **kwargs):
            self.set_feature_calls.append((args, kwargs))

    fake_parser = FakeParser()

    monkeypatch.setattr(views, "make_parser", lambda: fake_parser)

    # Avoid parsing; just ensure parseString is called with our parser and yields a minimal structure.
    class _Node:
        tagName = "text"

        def toxml(self):
            return "<text>ok</text>"

    def fake_parseString(_xml, parser=None):
        assert parser is fake_parser
        return [(views.START_ELEMENT, _Node())]

    monkeypatch.setattr(views, "parseString", fake_parseString)

    # Avoid DB update
    class _Q:
        def update(self, **kwargs):
            return 1

    class _Comments:
        objects = type("O", (), {"filter": staticmethod(lambda **kwargs: _Q())})()

    monkeypatch.setattr(views, "comments", _Comments)

    class _Req:
        user = type("U", (), {"is_authenticated": True})()
        body = b"<text>ok</text>"

    views.xxe_parse(_Req())

    assert fake_parser.set_feature_calls == []
