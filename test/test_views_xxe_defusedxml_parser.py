from xml.sax.handler import feature_external_ges


def test_uses_defusedxml_make_parser_and_disables_external_entities(mocker):
    """Regression test for XXE mitigation.

    Patch changed import to defusedxml.sax.make_parser and sets external general entities to False.
    Ensure xxe_parse calls make_parser and disables feature_external_ges.
    """

    from introduction import views

    parser_mock = mocker.Mock()
    make_parser_mock = mocker.patch.object(views, "make_parser", return_value=parser_mock)

    mocker.patch.object(views, "parseString", return_value=[])

    class _Req:
        body = b"<root/>"

    views.xxe_parse(_Req())

    make_parser_mock.assert_called_once()
    parser_mock.setFeature.assert_called_once_with(feature_external_ges, False)
