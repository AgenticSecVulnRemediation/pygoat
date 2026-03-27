import types
import pytest

# Assumptions:
# - Django is available and introduction.views can be imported.
# - We unit-test the changed behavior: parser disables external-general-entities via explicit feature URI.


def test_xxe_parse_disables_external_general_entities_by_uri(mocker):
    # Arrange
    import introduction.views as views

    request = types.SimpleNamespace()
    request.user = types.SimpleNamespace(is_authenticated=True)
    request.body = b"<xml><text>hi</text></xml>"

    parser = mocker.Mock()
    make_parser_mock = mocker.patch.object(views, "make_parser", return_value=parser)

    # Stop after feature set; we only validate the new setFeature call.
    mocker.patch.object(views, "parseString", side_effect=Exception("stop"))
    mocker.patch.object(views, "HttpResponseBadRequest", return_value="BAD_REQUEST")

    # Act
    views.xxe_parse(request)

    # Assert
    make_parser_mock.assert_called_once()
    parser.setFeature.assert_any_call("http://xml.org/sax/features/external-general-entities", False)
