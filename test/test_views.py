import pytest


def test_xxe_parse_uses_defusedxml_make_parser(monkeypatch):
    """Delta test: ensure defusedxml.sax.make_parser is used for XXE parsing."""

    import introduction.views as views

    assert views.make_parser.__module__.startswith('defusedxml')
