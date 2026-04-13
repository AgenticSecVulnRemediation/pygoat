import pytest


# Delta covered: make_parser imported from defusedxml.sax instead of xml.sax.
# This reduces XXE risk by using hardened parser defaults.

def test_views_imports_defusedxml_sax_make_parser():
    from pathlib import Path

    path = Path('introduction/views.py')
    content = path.read_text(encoding='utf-8')

    assert 'from defusedxml.sax import make_parser' in content
    assert 'from xml.sax import make_parser' not in content
