import pytest


# Path derived from source file: introduction/views.py
from introduction import views


def test_xxe_parse_disables_external_general_entities(mocker):
    # Arrange
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.body = b"<root><text>hello</text></root>"

    # Mock XML parsing to avoid real XML processing while asserting security flag
    parser = mocker.Mock()
    make_parser_mock = mocker.patch("introduction.views.make_parser", return_value=parser)

    # parseString returns an iterable of events
    doc_iter = [(views.START_ELEMENT, mocker.Mock(tagName='text', toxml=mocker.Mock(return_value='<text>hello</text>')))]
    parse_string_mock = mocker.patch("introduction.views.parseString", return_value=doc_iter)

    # Mock node expansion call
    doc_iter[0][1].expandNode = mocker.Mock()

    mocker.patch("introduction.views.comments.objects.filter", return_value=mocker.Mock(update=mocker.Mock(return_value=1)))
    mocker.patch("introduction.views.render", return_value=mocker.Mock())

    # Act
    views.xxe_parse(request)

    # Assert
    parser.setFeature.assert_called_once_with(views.feature_external_ges, False)
