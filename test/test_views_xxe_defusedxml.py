import pytest


def test_xxe_parse_uses_defusedxml_pulldom():
    """Delta test: ensure views imports defusedxml.pulldom instead of xml.dom.pulldom."""
    import introduction.views as views

    assert views.parseString.__module__.startswith('defusedxml')
