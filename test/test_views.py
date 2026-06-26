# Assumptions:
# - The Django app package is named `introduction` and is importable during tests.
# - These tests use pytest and monkeypatch to avoid hitting the database.

import types

import pytest


@pytest.mark.parametrize(
    "parser_module",
    [
        # New secure behavior: make_parser comes from defusedxml.sax
        "defusedxml.sax",
    ],
)
def test_views_uses_defusedxml_sax_make_parser(parser_module):
    """Delta test for PR #1947: ensure XXE parser is sourced from defusedxml.sax."""
    import introduction.views as views

    assert views.make_parser.__module__ == parser_module
