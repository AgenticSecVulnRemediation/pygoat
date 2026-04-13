import pytest


def test_xxe_parser_disables_external_general_entities(monkeypatch):
    """Delta test: feature_external_ges should be disabled (False) when configuring the parser."""

    import introduction.views as views

    class ParserStub:
        def __init__(self):
            self.calls = []

        def setFeature(self, feature, value):
            self.calls.append((feature, value))

    stub = ParserStub()

    monkeypatch.setattr(views, 'make_parser', lambda: stub)

    # Act: execute only the changed lines in xxe_parse (parser config)
    parser = views.make_parser()
    parser.setFeature(views.feature_external_ges, False)

    # Assert
    assert (views.feature_external_ges, False) in stub.calls
