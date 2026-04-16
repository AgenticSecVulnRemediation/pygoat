import types

import pytest

# Assumption: repository root is on PYTHONPATH in test runner.
from introduction import views


def test_xxe_parse_uses_defusedxml_make_parser_import():
    # Regression test for XXE hardening change: make_parser import should come from defusedxml.sax
    assert views.make_parser.__module__.startswith("defusedxml")
