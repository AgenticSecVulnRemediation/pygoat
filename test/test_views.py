# Assumptions:
# - This repo uses pytest for Python testing.

import pytest


def test_xxe_parse_uses_defusedxml_and_sets_empty_string_when_no_text_child(mocker):
    """Delta: xxe_parse now uses defusedxml minidom, and safely handles missing text."""
    from introduction import views

    request = mocker.Mock()
    request.body = b"<root><text/></root>"

    parse_spy = mocker.spy(views, "parseString")
    update_mock = mocker.Mock()
    views.comments.objects.filter.return_value.update = update_mock

    views.xxe_parse(request)

    parse_spy.assert_called_once_with("<root><text/></root>")
    update_mock.assert_called_once_with(comment="")
