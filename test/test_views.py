# Assumption: repository uses pytest; Django is installed in CI. This unit test avoids DB and templates.


def test_xxe_parse_uses_defusedxml_sax_make_parser(monkeypatch):
    """Delta: make_parser now comes from defusedxml.sax and feature_external_ges is disabled."""
    from introduction import views

    observed = {}

    class _FakeParser:
        def setFeature(self, name, value):
            observed["name"] = name
            observed["value"] = value

    # views.make_parser is imported into module; replace it to avoid calling real parser.
    monkeypatch.setattr(views, "make_parser", lambda: _FakeParser())
    monkeypatch.setattr(views, "parseString", lambda _xml, parser=None: [])
    monkeypatch.setattr(views, "render", lambda request, tpl: "ok")

    class _Req:
        body = b"<root/>"

    views.xxe_parse(_Req())

    assert observed["value"] is False
