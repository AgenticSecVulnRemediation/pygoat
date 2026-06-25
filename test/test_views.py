# Assumption: Django app module is named `introduction`.
# This test targets the delta: ensuring pulldom parseString is imported from defusedxml.pulldom.


def test_views_uses_defusedxml_pulldom_parseString():
    import introduction.views as views

    assert views.parseString.__module__.startswith(
        "defusedxml.pulldom"
    ), "parseString should come from defusedxml.pulldom after the fix"
