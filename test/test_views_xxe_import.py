import pytest

# Assumption: repository root is on PYTHONPATH in test runner.
from introduction import views


def test_views_uses_defusedxml_sax_make_parser():
    assert views.make_parser.__module__.startswith("defusedxml")
