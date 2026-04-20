import types

import pytest


def test_xxe_parse_disables_external_general_entities(monkeypatch):
    """Delta test: xxe_parse now sets feature_external_ges to False.

    We patch make_parser to capture setFeature calls and ensure it's invoked with False.
    """

    import introduction.views as views

    class DummyParser:
        def __init__(self):
            self.calls = []

        def setFeature(self, feature, value):
            self.calls.append((feature, value))

    dummy_parser = DummyParser()

    def fake_make_parser():
        return dummy_parser

    # Avoid pulling in real XML parser behavior
    def fake_parse_string(xml, parser=None):
        # Simulate minimal pulldom iteration contract used by xxe_parse
        def gen():
            yield (None, None)
        return gen()

    # Ensure xxe_parse does not crash on 'text' usage; make it set a default text
    def fake_iter(doc):
        return iter([])

    monkeypatch.setattr(views, "make_parser", fake_make_parser)
    monkeypatch.setattr(views, "parseString", fake_parse_string)

    # Patch START_ELEMENT constant and update body decode path
    monkeypatch.setattr(views, "START_ELEMENT", object())

    class DummyRequest:
        def __init__(self):
            self.user = types.SimpleNamespace(is_authenticated=True)
            self.body = b"<root/>"

    # Prevent DB update and template render
    monkeypatch.setattr(views, "comments", types.SimpleNamespace(objects=types.SimpleNamespace(filter=lambda **kwargs: types.SimpleNamespace(update=lambda **kw: 1))))
    monkeypatch.setattr(views, "render", lambda request, template, context=None: (template, context))

    # Act
    views.xxe_parse(DummyRequest())

    # Assert
    from xml.sax.handler import feature_external_ges
    assert (feature_external_ges, False) in dummy_parser.calls
