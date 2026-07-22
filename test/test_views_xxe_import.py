import types
import pytest


def test_views_import_uses_defusedxml_sax_make_parser(monkeypatch):
    # Regression test for XXE hardening: ensure defusedxml.sax.make_parser is imported/used.
    import pkgutil

    data = pkgutil.get_data('introduction', 'views.py')
    assert data is not None
    src = data.decode('utf-8')

    assert 'from defusedxml.sax import make_parser' in src
