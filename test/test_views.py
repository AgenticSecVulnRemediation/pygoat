import pytest


def test_views_uses_defusedxml_pulldom_import():
    # Delta test for XXE hardening: ensure defusedxml.pulldom is used.
    # This is a lightweight import-level assertion.
    import introduction.views as views

    assert views.parseString.__module__.startswith('defusedxml')
