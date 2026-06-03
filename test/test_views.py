import introduction.views as views


def test_views_uses_defusedxml_sax_make_parser():
    """Regression: views must import make_parser from defusedxml.sax."""
    assert views.make_parser.__module__.startswith("defusedxml"), (
        f"Expected defusedxml.sax make_parser, got {views.make_parser.__module__}"
    )
