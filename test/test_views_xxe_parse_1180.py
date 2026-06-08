import types
import pytest

import introduction.views as views


def test_xxe_parse_uses_defusedxml_minidom_parseString(monkeypatch):
    """Regression: ensure defusedxml minidom parseString is used instead of xml.dom.pulldom parsing."""

    # If old pulldom START_ELEMENT existed in module, it would indicate old approach.
    assert not hasattr(views, 'START_ELEMENT')

    seen = {'called': False}

    def _fake_parse(xml_str):
        seen['called'] = True

        class _Doc:
            def getElementsByTagName(self, name):
                class _N:
                    def toxml(self):
                        return '<text>hi</text>'
                return [_N()]

        return _Doc()

    monkeypatch.setattr(views, 'parseString', _fake_parse)

    class _Req:
        user = types.SimpleNamespace(is_authenticated=True)
        body = b'<text>hi</text>'

    monkeypatch.setattr(views, 'render', lambda request, template, context=None: {'template': template, 'context': context})

    views.xxe_parse(_Req())
    assert seen['called'] is True
