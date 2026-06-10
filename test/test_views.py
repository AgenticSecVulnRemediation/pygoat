import pytest

import introduction.views as views


class _User:
    def __init__(self, authenticated: bool):
        self.is_authenticated = authenticated


class _Request:
    def __init__(self, authenticated: bool, body: bytes):
        self.user = _User(authenticated)
        self.method = "POST"
        self.body = body


def test_xxe_parse_disables_external_general_entities(mocker):
    """Regression test: XXE parsing must disable external general entities (feature_external_ges=False)."""

    # Arrange
    req = _Request(authenticated=True, body=b"<root><text>hello</text></root>")

    parser_mock = mocker.Mock()
    make_parser_spy = mocker.patch.object(views, "make_parser", return_value=parser_mock)

    # Provide a minimal pulldom iterator result for parseString consumption
    class _Node:
        tagName = "text"

        def toxml(self):
            return "<text>hello</text>"

    mocker.patch.object(views, "parseString", return_value=[(views.START_ELEMENT, _Node())])

    mocker.patch.object(views.comments.objects, "filter", return_value=mocker.Mock(update=mocker.Mock(return_value=1)))
    mocker.patch.object(views, "render", return_value="rendered")

    # Act
    result = views.xxe_parse(req)

    # Assert
    assert result == "rendered"
    make_parser_spy.assert_called_once()
    parser_mock.setFeature.assert_called_once_with(views.feature_external_ges, False)
