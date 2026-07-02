import pathlib


def test_views_imports_defusedxml_make_parser():
    """Regression test: XXE hardening should use defusedxml.sax.make_parser, not xml.sax.make_parser."""
    content = pathlib.Path('introduction/views.py').read_text(encoding='utf-8')
    assert 'from defusedxml.sax import make_parser' in content
    assert 'from xml.sax import make_parser' not in content
