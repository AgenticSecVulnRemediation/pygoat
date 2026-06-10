import pytest


def test_views_imports_pulldom_from_defusedxml():
    """Delta test: prevent XXE by ensuring defusedxml.pulldom is used."""

    import introduction.views as views

    # START_ELEMENT constant is defined in pulldom modules; validate it originates from defusedxml.
    assert views.START_ELEMENT.__module__.startswith("defusedxml"), (
        "Expected START_ELEMENT from defusedxml.pulldom"
    )
