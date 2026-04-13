import pytest


def test_xxe_parse_uses_defusedxml_make_parser(monkeypatch):
    """Delta test: ensure introduction.views uses defusedxml.sax.make_parser, not xml.sax.make_parser."""

    # Import module under test
    import introduction.views as views

    # Act/Assert
    # The patch changed the import to: from defusedxml.sax import make_parser
    assert views.make_parser.__module__.startswith('defusedxml')
