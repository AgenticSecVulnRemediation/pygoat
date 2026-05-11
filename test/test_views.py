# Assumption: repository uses pytest; Django is installed in CI. This test asserts the delta import behavior.


def test_views_make_parser_comes_from_defusedxml_sax():
    """Delta: make_parser import switched to defusedxml.sax.make_parser."""
    from introduction import views

    # defusedxml.sax.make_parser should originate from module 'defusedxml.sax'
    assert getattr(views.make_parser, "__module__", "") == "defusedxml.sax"
