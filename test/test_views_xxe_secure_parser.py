import pytest


def test_xxe_parse_uses_defusedxml_secure_parser_comment_present():
    """Regression test for XXE fix: ensure the code no longer enables external entities."""
    from pathlib import Path

    content = Path('introduction/views.py').read_text(encoding='utf-8')

    assert 'from defusedxml.sax import make_parser' in content
    assert 'feature_external_ges' not in content or 'setFeature(feature_external_ges' not in content
    assert 'External entity processing is disabled' in content
