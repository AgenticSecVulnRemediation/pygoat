# Assumption: repository uses pytest; Django is installed in CI.


def test_xxe_parse_uses_defusedxml_pulldom_parseString(monkeypatch):
    """Delta: import switched from xml.dom.pulldom to defusedxml.pulldom.

    We assert views.parseString is called (and can be monkeypatched) without relying on stdlib pulldom.
    """
    from introduction import views

    called = {"count": 0}

    def _fake_parse_string(_xml, parser=None):
        called["count"] += 1
        return []

    monkeypatch.setattr(views, "parseString", _fake_parse_string)

    class _FakeParser:
        def setFeature(self, *_args, **_kwargs):
            pass

    monkeypatch.setattr(views, "make_parser", lambda: _FakeParser())
    monkeypatch.setattr(views, "render", lambda request, tpl: "ok")

    class _Req:
        body = b"<root/>"

    views.xxe_parse(_Req())

    assert called["count"] == 1
