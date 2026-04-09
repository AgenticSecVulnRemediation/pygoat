import pytest

# Assumption: module import path is introduction.views
import introduction.views as views


def test_xxe_parse_disables_external_general_entities(mocker):
    # Arrange
    parser = mocker.Mock()
    make_parser_mock = mocker.patch.object(views, 'make_parser', return_value=parser)

    # parseString returns an iterable; keep it empty so function doesn't depend on XML parsing here
    mocker.patch.object(views, 'parseString', return_value=[])

    request = mocker.Mock()
    request.body = b'<root></root>'

    # Act
    with pytest.raises(UnboundLocalError):
        # Function expects to find <text> element and will reference 'text' otherwise.
        # We only assert the security-relevant behavior: feature_external_ges is set to False.
        views.xxe_parse(request)

    # Assert
    make_parser_mock.assert_called_once()
    parser.setFeature.assert_called_once_with(views.feature_external_ges, False)
