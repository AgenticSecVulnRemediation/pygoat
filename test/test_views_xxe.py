# Assumptions:
# - This repo uses pytest and pytest-mock.


def test_xxe_parse_sets_empty_string_when_text_element_missing_child(mocker):
    """Delta: safe handling for <text/> (no firstChild) should set empty string."""
    from introduction import views

    request = mocker.Mock()
    request.body = b"<root><text/></root>"

    parse_spy = mocker.spy(views, "parseString")
    update_mock = mocker.Mock()
    views.comments.objects.filter.return_value.update = update_mock

    views.xxe_parse(request)

    parse_spy.assert_called_once_with("<root><text/></root>")
    update_mock.assert_called_once_with(comment="")
