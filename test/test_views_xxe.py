import pytest


@pytest.mark.django_db
def test_xxe_parse_disables_external_general_entities(mocker):
    """Regression: XXE fix disables external general entities in SAX parser."""
    from introduction import views

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        user = DummyUser()
        body = b"<root><text>hello</text></root>"

    parser = mocker.Mock()
    mocker.patch.object(views, "make_parser", return_value=parser)

    # Return a dummy doc iterator that yields a text node
    class Node:
        tagName = "text"

        def toxml(self):
            return "<text>hello</text>"

    dummy_doc = [(views.START_ELEMENT, Node())]
    mocker.patch.object(views, "parseString", return_value=dummy_doc)

    # comments ORM calls
    mocker.patch.object(views.comments.objects, "filter", return_value=mocker.Mock(update=mocker.Mock()))
    mocker.patch.object(views, "render", return_value=mocker.Mock(status_code=200))

    # Act
    resp = views.xxe_parse(DummyRequest())

    # Assert
    parser.setFeature.assert_called_once_with(views.feature_external_ges, False)
    assert resp.status_code == 200
