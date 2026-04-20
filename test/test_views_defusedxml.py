import pytest


def test_views_uses_defusedxml_pulldom_import():
    from pathlib import Path

    content = Path('introduction/views.py').read_text(encoding='utf-8')
    assert 'from defusedxml.pulldom import START_ELEMENT, parseString' in content
