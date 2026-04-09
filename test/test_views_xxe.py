import pytest

# Assumption: module import path is introduction.views
import introduction.views as views


def test_xxe_parse_disables_external_general_entities_without_executing_xml_parse(mocker):
    # Arrange
    parser = mocker.Mock()
    mocker.patch.object(views, 'make_parser', return_value=parser)

    # Stop execution immediately after the security-relevant call.
    def _set_feature_side_effect(*args, **kwargs):
        raise RuntimeError('stop-after-setFeature')

    parser.setFeature.side_effect = _set_feature_side_effect

    request = mocker.Mock()
    request.body = b'<root></root>'

    # Act
    with pytest.raises(RuntimeError, match='stop-after-setFeature'):
        views.xxe_parse(request)

    # Assert
    parser.setFeature.assert_called_once_with(views.feature_external_ges, False)
