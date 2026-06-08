import pytest


def test_xxe_uses_defusedxml_pulldom_parseString(monkeypatch):
    """Delta test: ensure START_ELEMENT/parseString are imported from defusedxml.pulldom.

    This verifies the regression fix away from xml.dom.pulldom (XXE hardening).
    """
    # Import the module under test
    import introduction.views as views

    # Assert module came from defusedxml (and not stdlib xml.dom)
    assert views.parseString.__module__.startswith('defusedxml.')
    assert views.START_ELEMENT.__module__.startswith('defusedxml.')
