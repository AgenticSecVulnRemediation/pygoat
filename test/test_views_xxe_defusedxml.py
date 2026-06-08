import pytest

from introduction import views


class _DummyUser:
    is_authenticated = True


class _DummyRequest:
    def __init__(self, xml_payload: str):
        self.method = "POST"
        self.user = _DummyUser()
        self.body = xml_payload.encode("utf-8")


def test_xxe_parse_disables_external_general_entities(mocker):
    """Regression test for XXE fix: feature_external_ges must be set to False."""
    # Arrange
    mock_make_parser = mocker.patch.object(views, "make_parser", autospec=True)
    parser = mocker.Mock()
    mock_make_parser.return_value = parser

    # ParseString is used after setting the feature; stub it to avoid real XML parsing
    mocker.patch.object(views, "parseString", autospec=True, return_value=[])

    req = _DummyRequest("<?xml version='1.0'?><root><text>hi</text></root>")

    # Act
    views.xxe_parse(req)

    # Assert: ensure XXE-hardening toggle
    parser.setFeature.assert_any_call(views.feature_external_ges, False)
