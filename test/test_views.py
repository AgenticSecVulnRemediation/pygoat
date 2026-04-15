import pytest

from introduction import views


def test_views_uses_defusedxml_pulldom_parsestring():
    assert views.parseString.__module__.startswith("defusedxml"), (
        "Expected parseString to come from defusedxml to mitigate XXE"
    )
