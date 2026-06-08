import importlib


def test_views_uses_defusedxml_sax_make_parser():
    """Regression: views should import make_parser from defusedxml.sax."""
    views = importlib.import_module('introduction.views')

    assert views.make_parser.__module__.startswith('defusedxml.sax')
