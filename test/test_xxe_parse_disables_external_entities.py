from xml.sax.handler import feature_external_ges

import pytest


def test_xxe_parse_disables_external_general_entities(mocker):
    """Regression test for XXE mitigation.

    Patch changed xxe_parse to setFeature(feature_external_ges, False).
    Ensure the parser has external entity processing disabled.
    """

    from introduction import views

    parser_mock = mocker.Mock()
    mocker.patch.object(views, "make_parser", return_value=parser_mock)

    # parseString iterates events; return empty iterable to keep test minimal.
    mocker.patch.object(views, "parseString", return_value=[])

    class _Req:
        body = b"<root/>"

    views.xxe_parse(_Req())

    parser_mock.setFeature.assert_called_once_with(feature_external_ges, False)
