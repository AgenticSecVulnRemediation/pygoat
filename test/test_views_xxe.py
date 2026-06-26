import pytest


# Assumption: "introduction.views" is importable and contains the fixed xxe_parse.
from introduction import views


def test_xxe_parse_does_not_enable_external_entities(mocker):
    """Regression for XXE: xxe_parse must not set feature_external_ges True."""
    # Arrange
    request = mocker.Mock()
    request.body = b"<root><text>hi</text></root>"

    parser = mocker.Mock()
    make_parser_mock = mocker.patch("introduction.views.make_parser", return_value=parser)

    # parseString should yield one START_ELEMENT event with tagName 'text'
    node = mocker.Mock()
    node.tagName = "text"
    node.toxml.return_value = "<text>hi</text>"

    doc_iter = [(views.START_ELEMENT, node)]

    class FakeDoc(list):
        def expandNode(self, _):
            return None

    parse_string_mock = mocker.patch(
        "introduction.views.parseString",
        return_value=FakeDoc(doc_iter),
    )

    comments_mgr = mocker.Mock()
    comments_mgr.filter.return_value.update.return_value = 1
    mocker.patch.object(views, "comments", mocker.Mock(objects=comments_mgr))

    render_mock = mocker.patch("introduction.views.render", return_value=mocker.Mock())

    # Act
    views.xxe_parse(request)

    # Assert
    make_parser_mock.assert_called_once()

    # Ensure parser.setFeature(feature_external_ges, True) is NOT called
    if parser.setFeature.call_args_list:
        assert (views.feature_external_ges, True) not in [c.args for c in parser.setFeature.call_args_list]

    parse_string_mock.assert_called_once()
    render_mock.assert_called_once()
