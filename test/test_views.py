import importlib


def test_views_uses_defusedxml_make_parser():
    # Arrange/Act
    views = importlib.import_module('introduction.views')

    # Assert
    assert 'defusedxml.sax' in views.make_parser.__module__
