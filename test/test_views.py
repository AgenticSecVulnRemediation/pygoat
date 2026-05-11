# Assumption: repository uses pytest; Django is installed in CI.


def test_xxe_parse_uses_defused_sax_make_parser(monkeypatch):
    """Delta: views imports defusedxml.sax as defused_sax and uses it for parser creation."""
    from introduction import views

    observed = {"called": 0}

    class _FakeParser:
        pass

    def _fake_make_parser():
        observed["called"] += 1
        return _FakeParser()

    monkeypatch.setattr(views.defused_sax, "make_parser", _fake_make_parser)
    monkeypatch.setattr(views, "parseString", lambda _xml, parser=None: [])
    monkeypatch.setattr(views, "render", lambda request, tpl: "ok")

    class _Req:
        body = b"<root/>"

    views.xxe_parse(_Req())

    assert observed["called"] == 1
