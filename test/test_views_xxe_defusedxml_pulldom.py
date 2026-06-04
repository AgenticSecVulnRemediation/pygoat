import pytest


# Assumption: module path is importable from repo root.
import introduction.views as views


def test_xxe_uses_defusedxml_pulldom_parseString():
    # The patch changes xml.dom.pulldom.parseString to defusedxml.pulldom.parseString
    assert "defusedxml" in getattr(views.parseString, "__module__", "")
