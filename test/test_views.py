import pytest


def test_pulldom_parseString_is_defusedxml(monkeypatch):
    """Delta test: views should use defusedxml.pulldom.parseString to reduce XML attack surface."""

    import introduction.views as views

    assert views.parseString.__module__.startswith('defusedxml')
    assert views.START_ELEMENT.__module__.startswith('defusedxml')
