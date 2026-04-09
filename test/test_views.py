import introduction.views as views


def test_views_uses_defusedxml_sax_make_parser():
    # Assert the security fix: defusedxml.sax.make_parser is the one referenced by views.make_parser
    import defusedxml.sax as defused_sax

    assert views.make_parser is defused_sax.make_parser
