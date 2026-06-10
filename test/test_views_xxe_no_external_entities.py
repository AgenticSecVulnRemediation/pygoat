import pytest


def test_views_xxe_parse_does_not_enable_external_general_entities():
    """Regression test: defusedxml.sax parser should be used and external entities should not be enabled."""

    import introduction.views as views

    # Arrange: patch make_parser to a controllable fake
    parser = pytest.MonkeyPatch()

    class _FakeParser:
        def __init__(self):
            self.features = []

        def setFeature(self, feature, value):
            self.features.append((feature, value))

    fake = _FakeParser()

    # monkeypatch make_parser in views module
    mp = pytest.MonkeyPatch()
    mp.setattr(views, "make_parser", lambda: fake)

    # Also patch parseString to avoid real XML parsing; we just need it called.
    mp.setattr(views, "parseString", lambda *args, **kwargs: [])

    class _Req:
        user = type("U", (), {"is_authenticated": True})()
        body = b"<root/>"

    try:
        views.xxe_parse(_Req())
        # Assert: no external-ges feature enabling call happened
        assert not any(val is True for (_feat, val) in fake.features)
    finally:
        mp.undo()
