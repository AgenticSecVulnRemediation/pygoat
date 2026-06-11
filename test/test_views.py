# Assumptions:
# - This repository uses pytest.
# - The Django views module is importable as introduction.views.
# - We only unit-test the behavior changed by the patch: using defusedxml.pulldom.parseString.

import sys
import types
import importlib

import pytest


@pytest.fixture
def views_with_fake_defusedxml(monkeypatch):
    """Import introduction.views with a fake defusedxml.pulldom module to assert it is used."""

    # Create a fake defusedxml.pulldom module with sentinel members
    pulldom_mod = types.ModuleType("defusedxml.pulldom")
    sentinel_start = object()

    def sentinel_parse_string(*args, **kwargs):
        raise RuntimeError("sentinel parseString called")

    pulldom_mod.START_ELEMENT = sentinel_start
    pulldom_mod.parseString = sentinel_parse_string

    # Ensure package structure exists in sys.modules
    monkeypatch.setitem(sys.modules, "defusedxml", types.ModuleType("defusedxml"))
    monkeypatch.setitem(sys.modules, "defusedxml.pulldom", pulldom_mod)

    # Clear cached import to force re-evaluation of imports
    if "introduction.views" in sys.modules:
        del sys.modules["introduction.views"]

    return importlib.import_module("introduction.views"), pulldom_mod


def test_views_imports_parseString_from_defusedxml_pulldom(views_with_fake_defusedxml):
    views, pulldom_mod = views_with_fake_defusedxml

    # Assert the module-level import was sourced from defusedxml.pulldom
    assert views.parseString is pulldom_mod.parseString
    assert views.START_ELEMENT is pulldom_mod.START_ELEMENT
