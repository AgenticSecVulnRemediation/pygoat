import pytest


def test_views_uses_defusedxml_pulldom_parseString():
    """Delta regression test: import should be switched to defusedxml.pulldom."""
    import introduction.views as views

    assert views.parseString.__module__.startswith("defusedxml.pulldom")
