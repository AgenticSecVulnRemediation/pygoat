import pytest


def test_views_uses_defusedxml_make_parser_import_comment_variant():
    # Regression test: ensure XXE parser creation uses defusedxml.sax.make_parser.
    from pathlib import Path

    py_path = Path('introduction/views.py')
    content = py_path.read_text(encoding='utf-8')

    assert 'from defusedxml.sax import make_parser' in content
    assert 'from xml.sax import make_parser' not in content
