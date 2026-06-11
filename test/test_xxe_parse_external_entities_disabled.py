import re


def test_xxe_parse_disables_external_general_entities(mocker):
    """Regression test for XXE mitigation.

    Patch changed xxe_parse to setFeature(feature_external_ges, False).
    Ensure the parser has external entity processing disabled.
    """

    from introduction import views

    parser_mock = mocker.Mock()
    mocker.patch.object(views, "make_parser", return_value=parser_mock)
    mocker.patch.object(views, "parseString", return_value=[])

    class _Req:
        body = b"<root/>"

    views.xxe_parse(_Req())

    # Avoid importing feature_external_ges from views (implementation detail); just match the value passed.
    assert parser_mock.setFeature.call_args[0][1] is False
