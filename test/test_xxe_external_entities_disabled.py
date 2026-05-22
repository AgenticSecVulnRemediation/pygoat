from django.test import RequestFactory

import pytest

from introduction import views


def test_xxe_parse_disables_external_general_entities(mocker):
    """Regression test for XXE: parser must have external general entities disabled."""

    # Arrange
    rf = RequestFactory()
    req = rf.post(
        "/xxe/parse",
        data=b"<text>hello</text>",
        content_type="application/xml",
    )

    parser = mocker.Mock()
    make_parser_mock = mocker.patch.object(views, "make_parser", return_value=parser)

    # parseString returns an iterator over (event, node). Mock minimal behavior.
    node = mocker.Mock()
    node.tagName = "text"
    node.toxml.return_value = "<text>hello</text>"

    # The code iterates `for event, node in doc:` so doc must be iterable.
    doc_iterable = [(views.START_ELEMENT, node)]
    parse_string_mock = mocker.patch.object(views, "parseString", return_value=doc_iterable)

    # Also avoid DB update and template rendering side effects.
    mocker.patch.object(views.comments.objects, "filter")
    mocker.patch.object(views, "render", return_value=mocker.Mock())

    # Act
    views.xxe_parse(req)

    # Assert: feature_external_ges must be set to False (secure default).
    parser.setFeature.assert_any_call(views.feature_external_ges, False)
