import introduction.views as views


def test_xxe_parse_disables_external_general_entities(monkeypatch):
    """Regression test for XXE fix: external general entities should be disabled."""

    class DummyRequest:
        user = type("U", (), {"is_authenticated": True})()
        body = b"<root><text>hello</text></root>"

    # Capture feature flag passed to parser
    feature_values = {}

    class DummyParser:
        def setFeature(self, feature, value):
            feature_values[feature] = value

    class DummyDoc:
        def __iter__(self):
            return iter([])

    def fake_make_parser():
        return DummyParser()

    def fake_parseString(_xml, parser=None):
        return DummyDoc()

    def fake_render(_request, _template):
        return "OK"

    # Prevent DB update and avoid needing Django models
    class DummyComments:
        class objects:
            @staticmethod
            def filter(**_kwargs):
                return types.SimpleNamespace(update=lambda **_kw: None)

    monkeypatch.setattr(views, "make_parser", fake_make_parser)
    monkeypatch.setattr(views, "parseString", fake_parseString)
    monkeypatch.setattr(views, "render", fake_render)
    monkeypatch.setattr(views, "comments", DummyComments)

    views.xxe_parse(DummyRequest())

    assert views.feature_external_ges in feature_values
    assert feature_values[views.feature_external_ges] is False
