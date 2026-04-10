import importlib


def test_xxe_parse_disables_external_general_entities():
    # Arrange
    views = importlib.import_module('introduction.views')

    class FakeParser:
        def __init__(self):
            self.calls = []

        def setFeature(self, name, value):
            self.calls.append((name, value))

    fake_parser = FakeParser()

    def fake_make_parser():
        return fake_parser

    # Patch make_parser used by xxe_parse
    views.make_parser = fake_make_parser

    # Patch parseString to avoid real XML parsing; xxe_parse only needs it to be iterable
    def fake_parse_string(_xml, parser=None):
        assert parser is fake_parser
        return []

    views.parseString = fake_parse_string

    class DummyRequest:
        user = type('U', (), {'is_authenticated': True})()
        body = b'<root></root>'

    # Act
    views.xxe_parse(DummyRequest())

    # Assert
    assert ('http://xml.org/sax/features/external-general-entities', False) in fake_parser.calls
