import pytest

# Assumption: module path is importable as introduction.views
import introduction.views as views


def test_views_uses_defusedxml_pulldom_parseString(monkeypatch):
    # Assert the security fix: defusedxml.pulldom.parseString is the one referenced by views.parseString
    import defusedxml.pulldom as defused_pulldom

    assert views.parseString is defused_pulldom.parseString
    assert views.START_ELEMENT is defused_pulldom.START_ELEMENT
