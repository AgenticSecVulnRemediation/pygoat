import pytest


def test_xxe_parse_uses_defusedxml_pulldom_parseString():
    """Delta: START_ELEMENT/parseString now imported from defusedxml.pulldom."""
    from introduction import views

    assert views.parseString.__module__.startswith("defusedxml"), (
        f"Expected defusedxml parseString, got {views.parseString.__module__}"
    )
