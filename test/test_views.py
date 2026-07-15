import sys
import types

import pytest


def test_views_imports_defusedxml_pulldom(monkeypatch):
    """Regression test for XXE hardening: views.py must import defusedxml.pulldom, not xml.dom.pulldom."""

    # Arrange: create a fake defusedxml.pulldom module so import doesn't require the real dependency.
    pulldom_module = types.ModuleType("defusedxml.pulldom")
    pulldom_module.START_ELEMENT = object()

    def parse_string_stub(*args, **kwargs):
        raise AssertionError("parseString stub should not be executed in this import-only test")

    pulldom_module.parseString = parse_string_stub

    defusedxml_pkg = types.ModuleType("defusedxml")
    defusedxml_pkg.pulldom = pulldom_module

    monkeypatch.setitem(sys.modules, "defusedxml", defusedxml_pkg)
    monkeypatch.setitem(sys.modules, "defusedxml.pulldom", pulldom_module)

    # Ensure a clean import of introduction.views
    sys.modules.pop("introduction.views", None)

    # Act
    import introduction.views as views  # noqa: F401

    # Assert
    assert views.parseString is pulldom_module.parseString
    assert views.START_ELEMENT is pulldom_module.START_ELEMENT
