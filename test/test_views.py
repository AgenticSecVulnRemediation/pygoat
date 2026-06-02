# Assumption: The application is a Django project and imports resolve when running tests.
# These unit tests focus only on the security hardening introduced by switching to defusedxml.

import importlib


def test_views_uses_defusedxml_pulldom_import_for_xxe_defense():
    views = importlib.import_module("introduction.views")

    # The patch replaces xml.dom.pulldom.parseString with defusedxml.pulldom.parseString.
    # We assert the function wired into this module is from defusedxml.
    assert views.parseString.__module__.startswith("defusedxml"), (
        f"Expected defusedxml.parseString, got {views.parseString.__module__}"
    )
