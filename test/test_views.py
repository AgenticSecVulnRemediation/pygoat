import importlib
import sys
import types


def test_views_uses_defusedxml_pulldom_import():
    """Regression test for XXE: views must import pulldom from defusedxml, not xml.dom."""
    # Import module under test
    import introduction.views as views

    # Assert: module references parseString from defusedxml.pulldom
    assert views.parseString.__module__.startswith("defusedxml.pulldom")
