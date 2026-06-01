import pytest


def test_xxe_parse_disables_external_general_entities(monkeypatch):
    """Delta: xxe_parse now explicitly disables external-general-entities on the SAX parser."""
    from introduction import views

    class DummyParser:
        def __init__(self):
            self.features = []

        def setFeature(self, name, value):
            self.features.append((name, value))

    dummy_parser = DummyParser()

    # Patch make_parser used by xxe_parse
    monkeypatch.setattr(views, "make_parser", lambda: dummy_parser)

    # Avoid parsing; we only care about the feature flag call.
    def _fake_parse_string(_xml, parser=None):
        raise RuntimeError("stop after feature set")

    monkeypatch.setattr(views, "parseString", _fake_parse_string)

    with pytest.raises(RuntimeError):
        views.xxe_parse(type("Req", (), {"body": b"<x/>"})())

    assert (
        "http://xml.org/sax/features/external-general-entities",
        False,
    ) in dummy_parser.features
