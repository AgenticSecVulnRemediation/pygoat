import pytest


# Delta covered: pulldom parseString imported from defusedxml.pulldom.
# This test enforces that defusedxml is used for XML parsing import to mitigate XXE.

def test_views_imports_defusedxml_pulldom_parseString():
    from pathlib import Path

    path = Path('introduction/views.py')
    content = path.read_text(encoding='utf-8')

    assert 'from defusedxml.pulldom import START_ELEMENT, parseString' in content
