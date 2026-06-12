import types


def test_xxe_parse_disables_external_entity_processing(monkeypatch):
    # This test asserts the changed behavior: feature_external_ges is set to False.
    from introduction import views

    request = types.SimpleNamespace(
        user=types.SimpleNamespace(is_authenticated=True),
        body=b"<root><text>hello</text></root>",
    )

    class DummyParser:
        def __init__(self):
            self.features = []

        def setFeature(self, feature, value):
            self.features.append((feature, value))

    dummy_parser = DummyParser()

    monkeypatch.setattr(views, "make_parser", lambda: dummy_parser)

    # Avoid depending on real XML parsing and DB.
    class DummyDoc:
        def __iter__(self):
            return iter([])

    monkeypatch.setattr(views, "parseString", lambda _xml, parser=None: DummyDoc())
    monkeypatch.setattr(views, "render", lambda _req, _tmpl: ("ok"))

    # Act
    views.xxe_parse(request)

    # Assert
    assert (views.feature_external_ges, False) in dummy_parser.features
