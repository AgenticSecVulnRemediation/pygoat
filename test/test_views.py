import importlib


def test_views_imports_defusedxml_make_parser():
    # Assert the import is switched to defusedxml.sax.make_parser.
    import introduction.views as views

    importlib.reload(views)

    assert views.make_parser.__module__.startswith("defusedxml.sax")
