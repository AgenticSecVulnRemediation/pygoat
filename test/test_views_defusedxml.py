import pytest


def test_defusedxml_pulldom_import_is_used():
    """Regression: ensure the code path uses defusedxml rather than xml.dom.pulldom."""
    import introduction.views as views

    assert views.parseString.__module__.startswith("defusedxml.")
