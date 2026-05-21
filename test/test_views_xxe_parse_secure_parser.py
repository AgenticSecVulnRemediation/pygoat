import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import introduction.views as views  # noqa: E402


def test_xxe_parse_disables_external_general_entities(mocker):
    """Regression test: xxe_parse must disable external entities (feature_external_ges=False)."""
    # Arrange
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.body = b"<root><text>hello</text></root>"

    parser = mocker.Mock()
    make_parser_spy = mocker.patch.object(views, "make_parser", return_value=parser)

    # parseString is used as a generator via pulldom; stub it to avoid XML machinery.
    parse_string_spy = mocker.patch.object(views, "parseString", return_value=[])

    # patch comments model interaction to avoid DB
    comments = mocker.Mock()
    comments.objects.filter.return_value.update.return_value = 1
    mocker.patch.object(views, "comments", comments)

    # Act
    views.xxe_parse(request)

    # Assert
    make_parser_spy.assert_called_once()
    parser.setFeature.assert_any_call(views.feature_external_ges, False)
