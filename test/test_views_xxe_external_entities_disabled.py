import pytest


def test_xxe_parse_disables_external_general_entities(mocker):
    """Regression test: external general entities must be disabled (feature_external_ges=False)."""
    from introduction import views

    parser = mocker.Mock()
    make_parser = mocker.patch.object(views, "make_parser", autospec=True, return_value=parser)

    request = mocker.Mock()
    request.user.is_authenticated = True
    request.body = b"<root><text>hello</text></root>"

    # Prevent actual XML parsing; we only care about the parser feature flag call.
    mocker.patch.object(views, "parseString", autospec=True, return_value=[])
    mocker.patch.object(views.comments.objects, "filter", autospec=True)

    views.xxe_parse(request)

    make_parser.assert_called_once()
    parser.setFeature.assert_any_call(views.feature_external_ges, False)
