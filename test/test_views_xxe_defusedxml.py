import pytest


# Delta-focused tests for XXE hardening: views now uses defusedxml.sax.make_parser and
# no longer enables external general entities.


def _make_fake_request(xml_bytes: bytes):
    class _User:
        is_authenticated = True

    class _Req:
        user = _User()
        body = xml_bytes

    return _Req()


def test_xxe_parse_uses_defusedxml_make_parser(monkeypatch):
    from introduction import views

    called = {"make_parser": 0}

    def fake_make_parser():
        called["make_parser"] += 1
        return object()

    monkeypatch.setattr(views, "make_parser", fake_make_parser)

    # Provide a minimal doc/iterator to avoid real XML parsing.
    class _Doc:
        def __iter__(self):
            # START_ELEMENT is imported into module; tagName comparison expects 'text'
            class _Node:
                tagName = "text"

                def toxml(self):
                    return "<text>hello</text>"

            yield (views.START_ELEMENT, _Node())

        def expandNode(self, node):
            return None

    monkeypatch.setattr(views, "parseString", lambda *_args, **_kwargs: _Doc())

    # Prevent DB access and rendering side effects
    class _CommentsManager:
        def filter(self, **kwargs):
            return self

        def update(self, **kwargs):
            return 1

    monkeypatch.setattr(views, "comments", type("C", (), {"objects": _CommentsManager()})())
    monkeypatch.setattr(views, "render", lambda request, template, ctx=None: {"template": template, **(ctx or {})})

    req = _make_fake_request(b"<text>hello</text>")

    resp = views.xxe_parse(req)

    assert called["make_parser"] == 1
    assert resp["template"].endswith("xxe_lab.html")


def test_xxe_parse_does_not_set_feature_external_ges(monkeypatch):
    from introduction import views

    class ParserWithSetFeature:
        def __init__(self):
            self.set_feature_called = False

        def setFeature(self, *args, **kwargs):
            self.set_feature_called = True

    parser = ParserWithSetFeature()
    monkeypatch.setattr(views, "make_parser", lambda: parser)

    class _Doc:
        def __iter__(self):
            class _Node:
                tagName = "text"

                def toxml(self):
                    return "<text>hello</text>"

            yield (views.START_ELEMENT, _Node())

        def expandNode(self, node):
            return None

    monkeypatch.setattr(views, "parseString", lambda *_args, **_kwargs: _Doc())

    class _CommentsManager:
        def filter(self, **kwargs):
            return self

        def update(self, **kwargs):
            return 1

    monkeypatch.setattr(views, "comments", type("C", (), {"objects": _CommentsManager()})())
    monkeypatch.setattr(views, "render", lambda request, template, ctx=None: ctx or {})

    req = _make_fake_request(b"<text>hello</text>")
    views.xxe_parse(req)

    assert parser.set_feature_called is False
