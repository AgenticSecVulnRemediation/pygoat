import pytest


def test_views_uses_defusedxml_make_parser_import():
    """Regression test: ensure XXE parsing uses defusedxml.sax.make_parser import."""
    with open('introduction/views.py', 'r', encoding='utf-8') as f:
        src = f.read()

    assert 'from defusedxml.sax import make_parser' in src
