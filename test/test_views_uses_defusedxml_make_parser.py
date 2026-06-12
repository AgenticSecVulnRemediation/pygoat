import types


def test_views_imports_defusedxml_make_parser():
    # Ensures regression: we import make_parser from defusedxml, not xml.sax
    from introduction import views

    assert views.make_parser.__module__.startswith("defusedxml")
