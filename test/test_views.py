import pytest

# Assumptions:
# - Django project uses "introduction.views" module path.
# - Delta: XXE hardening uses defusedxml.sax.make_parser and disables external general entities.
from introduction import views


class _DummyUser:
    is_authenticated = True


class _DummyRequest:
    def __init__(self, body: bytes):
        self.body = body
        self.user = _DummyUser()


def test_xxe_parse_blocks_external_entity_expansion(monkeypatch):
    # Arrange: External entity payload that would be dangerous if expanded.
    xml = b"""<?xml version='1.0'?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM 'file:///etc/passwd'> ]>
<root><text>&xxe;</text></root>
"""
    req = _DummyRequest(xml)

    # Patch DB update & template rendering to avoid Django/DB dependencies
    class _Mgr:
        def filter(self, **kwargs):
            class _Q:
                def update(self, **kw):
                    return 1
            return _Q()

    monkeypatch.setattr(views, "comments", type("C", (), {"objects": _Mgr()})())
    monkeypatch.setattr(views, "render", lambda request, tpl, context=None: {"tpl": tpl, "ctx": context})

    # Act/Assert: defusedxml should raise on entity; at minimum, it must not succeed silently.
    with pytest.raises(Exception):
        views.xxe_parse(req)
