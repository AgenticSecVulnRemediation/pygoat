import pytest


def test_views_uses_defusedxml_make_parser_for_xxe(mocker):
    """Delta test: import switched from xml.sax.make_parser to defusedxml.sax.make_parser."""
    # Arrange
    imported = __import__("introduction.views", fromlist=["make_parser"])

    # Act
    mp = getattr(imported, "make_parser")

    # Assert
    assert mp.__module__.startswith("defusedxml"), f"Expected defusedxml make_parser, got: {mp.__module__}"
