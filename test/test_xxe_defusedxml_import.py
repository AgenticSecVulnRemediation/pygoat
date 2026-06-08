import pytest


def test_views_xxe_import_uses_defusedxml_pulldom():
    """Delta test: ensure XXE mitigation changes import to defusedxml.pulldom."""

    with open("introduction/views.py", "r", encoding="utf-8") as f:
        content = f.read()

    assert "from defusedxml.pulldom import START_ELEMENT, parseString" in content
    assert "from xml.dom.pulldom import START_ELEMENT, parseString" not in content
