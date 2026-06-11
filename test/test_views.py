# Assumptions:
# - This repository uses pytest.
# - The Django views module is importable as introduction.views.
# - We only unit-test the behavior changed by the patch: xml.sax.make_parser is sourced from defusedxml.sax.

import sys
import types
import importlib

import pytest


@pytest.fixture
def views_with_fake_defusedxml_sax(monkeypatch):
    """Import introduction.views with a fake defusedxml.sax module to assert it is used."""

    sax_mod = types.ModuleType("defusedxml.sax")

    def sentinel_make_parser(*args, **kwargs):
        raise RuntimeError("sentinel make_parser called")

    sax_mod.make_parser = sentinel_make_parser

    # Ensure package structure exists in sys.modules
    monkeypatch.setitem(sys.modules, "defusedxml", types.ModuleType("defusedxml"))
    monkeypatch.setitem(sys.modules, "defusedxml.sax", sax_mod)

    if "introduction.views" in sys.modules:
        del sys.modules["introduction.views"]

    return importlib.import_module("introduction.views"), sax_mod


def test_views_imports_make_parser_from_defusedxml_sax(views_with_fake_defusedxml_sax):
    views, sax_mod = views_with_fake_defusedxml_sax

    # Assert the module-level import was sourced from defusedxml.sax
    assert views.make_parser is sax_mod.make_parser
