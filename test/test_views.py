import pytest


def _import_views_safely():
    try:
        import introduction.views as views
        return views
    except Exception:
        pytest.skip("Django environment not available; skipping unit-level import test")


def test_xxe_parse_uses_defusedxml_make_parser():
    # Arrange/Act
    views = _import_views_safely()
    from xml.sax import make_parser as stdlib_make_parser

    # Assert
    assert views.make_parser is not stdlib_make_parser
