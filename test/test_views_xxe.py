import pytest


# Tests cover the XXE fix in introduction/views.py:
# parser.setFeature(feature_external_ges, False)


def test_xxe_parse_disables_external_general_entities(mocker):
    """Regression: xxe_parse must disable external general entities to prevent XXE."""
    from introduction import views

    parser = mocker.Mock()
    make_parser = mocker.patch('introduction.views.make_parser', return_value=parser)

    # Avoid actually parsing XML; the security fix is the feature flag.
    mocker.patch('introduction.views.parseString', return_value=[])

    class _Req:
        user = mocker.Mock(is_authenticated=True)
        body = b"<root/>"

    views.xxe_parse(_Req())

    make_parser.assert_called_once_with()
    parser.setFeature.assert_any_call(views.feature_external_ges, False)
