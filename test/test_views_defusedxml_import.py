import pytest


def test_views_imports_defusedxml_make_parser_instead_of_xml_sax_make_parser():
    # This is a delta test for the import-level security fix.
    # It asserts the source file now imports defusedxml.sax.make_parser.
    with open('introduction/views.py', 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'from defusedxml.sax import make_parser' in content
    assert 'from xml.sax import make_parser' not in content
