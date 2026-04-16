def test_views_uses_defusedxml_sax_make_parser_not_xml_sax():
    """Delta: views imports defusedxml.sax.make_parser instead of xml.sax.make_parser."""
    with open("introduction/views.py", "r", encoding="utf-8") as f:
        src = f.read()

    assert "from defusedxml.sax import make_parser" in src
    assert "from xml.sax import make_parser" not in src
