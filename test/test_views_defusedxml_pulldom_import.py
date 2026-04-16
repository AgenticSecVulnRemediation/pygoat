def test_views_uses_defusedxml_pulldom_not_stdlib_pulldom():
    """Delta: views imports defusedxml.pulldom instead of xml.dom.pulldom."""
    with open("introduction/views.py", "r", encoding="utf-8") as f:
        src = f.read()

    assert "from defusedxml.pulldom import START_ELEMENT, parseString" in src
    assert "from xml.dom.pulldom import START_ELEMENT, parseString" not in src
