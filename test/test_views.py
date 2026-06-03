import introduction.views as views


def test_views_uses_defusedxml_pulldom(monkeypatch):
    """Regression: views must import pulldom parser from defusedxml (hardening against unsafe XML)."""
    # The change is an import-level hardening. Assert the imported parseString originates from defusedxml.
    assert views.parseString.__module__.startswith("defusedxml"), (
        f"Expected defusedxml parseString, got {views.parseString.__module__}"
    )
