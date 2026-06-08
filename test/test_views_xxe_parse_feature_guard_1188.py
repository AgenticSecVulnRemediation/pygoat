# Assumption: Django app module is importable as `introduction.views` in test environment.
# This test targets the XXE mitigation change in xxe_parse: defusedxml SAX parser + disabling external entities.

import pytest


def _build_request(body: str, authenticated: bool = True):
    class _User:
        def __init__(self, authed: bool):
            self.is_authenticated = authed

    class _Req:
        def __init__(self, body_bytes: bytes, authed: bool):
            self.user = _User(authed)
            self.body = body_bytes

    return _Req(body.encode("utf-8"), authenticated)


def test_xxe_parse_when_external_entities_feature_setting_fails_returns_400(mocker):
    """Regression test for the patch:

    The patched code wraps `parser.setFeature(..., False)` in try/except and returns HttpResponseBadRequest
    when parser configuration fails. Previously this would raise and likely 500.
    """
    import introduction.views as views

    # Arrange
    request = _build_request("<root><text>hello</text></root>")

    parser_mock = mocker.Mock()
    parser_mock.setFeature.side_effect = Exception("boom")
    mocker.patch.object(views, "make_parser", return_value=parser_mock)

    # Act
    resp = views.xxe_parse(request)

    # Assert
    assert resp.status_code == 400
    assert b"XML parser configuration error" in resp.content
    parser_mock.setFeature.assert_called_once_with(
        "http://xml.org/sax/features/external-general-entities", False
    )
