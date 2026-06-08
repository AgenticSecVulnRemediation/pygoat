import pytest


def test_views_uses_defusedxml_sax_make_parser():
    """Delta test: ensure make_parser is imported from defusedxml.sax (XXE hardening)."""
    import introduction.views as views

    assert views.make_parser.__module__.startswith('defusedxml.')
