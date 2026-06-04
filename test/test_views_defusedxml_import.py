import pytest


def test_views_uses_defusedxml_pulldom_for_xxe_parsing():
    """Regression test: XXE parsing should use defusedxml's pulldom instead of xml.dom.pulldom."""
    from introduction import views

    assert views.parseString.__module__.startswith("defusedxml.")
