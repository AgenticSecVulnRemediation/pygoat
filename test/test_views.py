# Assumption: repository uses pytest; Django is installed in CI. This unit test avoids DB and templates.

import pytest


def test_xxe_parse_disables_external_general_entities(monkeypatch):
    """Delta: xxe_parse now sets feature_external_ges to False (previously True).

    We assert that parser.setFeature is invoked with False.
    """
    from introduction import views

    observed = {}

    class _FakeParser:
        def setFeature(self, name, value):
            observed["name"] = name
            observed["value"] = value

    def _fake_make_parser():
        return _FakeParser()

    # Ensure parseString returns an iterable that doesn't require real XML parsing.
    def _fake_parse_string(_xml, parser=None):
        return []

    monkeypatch.setattr(views, "make_parser", _fake_make_parser)
    monkeypatch.setattr(views, "parseString", _fake_parse_string)

    class _Req:
        body = b"<root/>"

    # Avoid template rendering dependency.
    monkeypatch.setattr(views, "render", lambda request, tpl: "ok")

    views.xxe_parse(_Req())

    assert observed.get("value") is False
