# Assumptions:
# - This repo uses pytest for Python testing.

import pytest


def test_xxe_parse_uses_defusedxml_and_reads_text_node_value(mocker):
    """Delta: xxe_parse now uses defusedxml.minidom.parseString and nodeValue extraction."""
    # Import inside test so the module import reflects the patched file
    from introduction import views

    # Arrange
    request = mocker.Mock()
    request.body = b"<root><text>Hello</text></root>"

    parse_spy = mocker.spy(views, "parseString")
    update_mock = mocker.Mock()
    views.comments.objects.filter.return_value.update = update_mock

    # Act
    views.xxe_parse(request)

    # Assert
    parse_spy.assert_called_once_with("<root><text>Hello</text></root>")
    update_mock.assert_called_once_with(comment="Hello")


def test_xxe_parse_missing_text_node_does_not_update_comment(mocker):
    """Delta: if no <text> element exists, function should not attempt update."""
    from introduction import views

    request = mocker.Mock()
    request.body = b"<root></root>"

    update_mock = mocker.Mock()
    views.comments.objects.filter.return_value.update = update_mock

    views.xxe_parse(request)

    update_mock.assert_not_called()
