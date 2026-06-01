import pytest


def test_xxe_parser_is_defusedxml_variant():
    """Delta: views.py switched make_parser import from xml.sax to defusedxml.sax."""
    # Import locally so test fails if the module import breaks
    from introduction import views

    assert views.make_parser.__module__.startswith("defusedxml"), (
        f"Expected defusedxml make_parser, got {views.make_parser.__module__}"
    )
