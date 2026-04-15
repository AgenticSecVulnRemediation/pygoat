import types

import pytest

from introduction import views


def test_xxe_parse_disables_external_general_entities(mocker):
    request = types.SimpleNamespace(user=types.SimpleNamespace(is_authenticated=True), body=b"<root><text>hi</text></root>")

    parser = mocker.Mock()
    make_parser = mocker.patch.object(views, "make_parser", return_value=parser)

    node = types.SimpleNamespace(tagName='text', toxml=lambda: '<text>hi</text>')
    doc_iter = [(views.START_ELEMENT, node)]
    doc = mocker.Mock()
    doc.__iter__ = lambda self: iter(doc_iter)
    doc.expandNode = mocker.Mock()
    mocker.patch.object(views, "parseString", return_value=doc)

    views.xxe_parse(request)

    make_parser.assert_called_once()
    parser.setFeature.assert_called_with(views.feature_external_ges, False)
