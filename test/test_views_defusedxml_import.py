import pytest


def test_xxe_parse_uses_defusedxml_pulldom_parseString(monkeypatch):
    """Delta test: ensure views imports parseString from defusedxml.pulldom, not xml.dom.pulldom."""

    from introduction import views

    assert views.parseString.__module__.startswith(
        "defusedxml"
    ), f"parseString should come from defusedxml, got {views.parseString.__module__}"
