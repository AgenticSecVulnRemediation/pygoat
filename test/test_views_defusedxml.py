import pytest


def test_defusedxml_sax_make_parser_is_used():
    """Regression: ensure the hardened parser factory is imported from defusedxml.sax."""
    import introduction.views as views

    assert views.make_parser.__module__.startswith("defusedxml.")
