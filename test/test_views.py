import types
import pytest

# Assumptions:
# - Django is available and introduction.views can be imported.
# - We unit-test the changed behavior: xxe_parse uses defusedxml.pulldom.parseString and returns 400 on parse errors.


def test_xxe_parse_returns_bad_request_when_defusedxml_parse_raises(mocker):
    # Arrange
    import introduction.views as views

    request = types.SimpleNamespace()
    request.user = types.SimpleNamespace(is_authenticated=True)
    request.body = b"<xml><text>hi</text></xml>"

    parse_mock = mocker.patch.object(views, "parseString", side_effect=Exception("boom"))
    bad_req_mock = mocker.patch.object(views, "HttpResponseBadRequest", return_value="BAD_REQUEST")
    mocker.patch.object(views.logging, "error")

    # Act
    resp = views.xxe_parse(request)

    # Assert
    assert resp == "BAD_REQUEST"
    parse_mock.assert_called_once()
    bad_req_mock.assert_called_once_with("Invalid XML data")
