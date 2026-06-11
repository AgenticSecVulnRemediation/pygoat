import pytest


def test_views_make_parser_is_from_defusedxml(monkeypatch):
    """Delta test: ensure make_parser imported from defusedxml.sax."""

    from introduction import views

    assert views.make_parser.__module__.startswith(
        "defusedxml"
    ), f"Expected defusedxml.sax.make_parser, got {views.make_parser.__module__}"
