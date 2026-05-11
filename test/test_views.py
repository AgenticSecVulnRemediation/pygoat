# Assumption: repository uses pytest; Django is installed in CI.


def test_xxe_parse_uses_defusedxml_sax_feature_external_ges_false(monkeypatch):
    """Delta: switched to defusedxml.sax and uses sax.handler.feature_external_ges with False."""
    from introduction import views

    observed = {}

    class _FakeParser:
        def setFeature(self, name, value):
            observed["name"] = name
            observed["value"] = value

    # Patch the defusedxml.sax namespace inside views
    monkeypatch.setattr(views.sax, "make_parser", lambda: _FakeParser())
    monkeypatch.setattr(views, "parseString", lambda _xml, parser=None: [])
    monkeypatch.setattr(views, "render", lambda request, tpl: "ok")

    class _Req:
        body = b"<root/>"

    views.xxe_parse(_Req())

    assert observed["value"] is False
