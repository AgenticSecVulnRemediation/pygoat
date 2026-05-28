import pytest


def test_views_uses_defusedxml_pulldom(monkeypatch):
    """Regression for defusedxml import change in views.py.

    Ensures START_ELEMENT/parseString are imported from defusedxml.pulldom.
    """
    from introduction import views

    # The imported objects should come from defusedxml module
    assert views.parseString.__module__.startswith('defusedxml')
    assert views.START_ELEMENT.__module__.startswith('defusedxml')
