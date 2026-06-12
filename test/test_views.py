import pytest


def test_xxe_parse_disables_external_entities(monkeypatch):
    """Regression: xxe_parse must set feature_external_ges to False."""
    # Import the module under test
    import introduction.views as views

    captured = {}

    class _FakeParser:
        def setFeature(self, feature, value):
            captured["feature"] = feature
            captured["value"] = value

    def fake_make_parser():
        return _FakeParser()

    monkeypatch.setattr(views, "make_parser", fake_make_parser)

    # Ensure parseString is called with our parser but doesn't do any real parsing
    class _FakeDoc:
        def __iter__(self):
            return iter([])

    monkeypatch.setattr(views, "parseString", lambda *_args, **_kwargs: _FakeDoc())

    # Avoid DB writes
    class _FakeFilter:
        def update(self, **_kwargs):
            return 1

    class _FakeCommentsObjects:
        @staticmethod
        def filter(**_kwargs):
            return _FakeFilter()

    monkeypatch.setattr(views, "comments", type("C", (), {"objects": _FakeCommentsObjects})())

    monkeypatch.setattr(views, "render", lambda *args, **kwargs: "rendered")

    class _Req:
        class user:
            is_authenticated = True

        body = b"<text>hello</text>"

    views.xxe_parse(_Req())

    assert captured["feature"] == views.feature_external_ges
    assert captured["value"] is False
