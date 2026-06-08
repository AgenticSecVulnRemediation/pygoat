# Assumptions:
# - This repo uses pytest and pytest-mock.


def test_xxe_parse_uses_parseString_on_decoded_body_and_updates_comment(mocker):
    """Delta: xxe_parse now uses a safer minidom parseString path + nodeValue extraction."""
    from introduction import views

    request = mocker.Mock()
    request.body = b"<root><text>Hello</text></root>"

    parse_spy = mocker.spy(views, "parseString")
    update_mock = mocker.Mock()
    views.comments.objects.filter.return_value.update = update_mock

    views.xxe_parse(request)

    parse_spy.assert_called_once_with("<root><text>Hello</text></root>")
    update_mock.assert_called_once_with(comment="Hello")
