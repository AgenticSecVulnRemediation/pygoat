import pytest


# Assumption: module path is importable from repo root.
import introduction.views as views


def test_xxe_uses_defusedxml_make_parser(mocker):
    # The patch changes import from xml.sax.make_parser to defusedxml.sax.make_parser.
    # We assert that views.make_parser is the defusedxml version by checking its module.
    assert "defusedxml" in getattr(views.make_parser, "__module__", "")
