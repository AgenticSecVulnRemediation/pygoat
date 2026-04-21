import pytest

# Assumption: tests run with project root on PYTHONPATH so `introduction` is importable.
from introduction import views


class DummyUser:
    is_authenticated = True


class DummyRequest:
    def __init__(self, body: bytes):
        self.user = DummyUser()
        self.body = body


def test_xxe_parse_disables_external_entities_feature(mocker):
    """Regression: XXE hardening should disable external general entities and use defusedxml parser."""
    # Arrange
    parser = mocker.Mock()
    make_parser_mock = mocker.patch.object(views, "make_parser", return_value=parser)

    # Ensure parseString returns an iterable of events and provides required methods on doc
    doc = mocker.Mock()
    doc.__iter__ = mocker.Mock(return_value=iter([]))
    mocker.patch.object(views, "parseString", return_value=doc)
    # Avoid DB update and template rendering
    comments_qs = mocker.Mock()
    comments_qs.update.return_value = 1
    mocker.patch.object(views.comments, "objects", mocker.Mock(filter=mocker.Mock(return_value=comments_qs)))
    mocker.patch.object(views, "render", return_value={"rendered": True})

    req = DummyRequest(b"<root><text>hello</text></root>")

    # Act
    views.xxe_parse(req)

    # Assert
    make_parser_mock.assert_called_once()
    parser.setFeature.assert_called_once_with(views.feature_external_ges, False)
