import types

import pytest


@pytest.mark.django_db
def test_xxe_parse_uses_defusedxml_and_returns_empty_on_bad_xml(mocker):
    """Delta behavior: xxe_parse no longer uses xml.sax external entities; parses via defusedxml.ElementTree.

    We assert that on malformed XML it does not raise and stores empty comment.
    """

    from introduction import views

    update_spy = mocker.patch.object(views.comments.objects, 'filter')
    update_spy.return_value.update = mocker.Mock()

    request = types.SimpleNamespace(
        user=types.SimpleNamespace(is_authenticated=True),
        body=b'<root><text>unclosed',
    )

    response = views.xxe_parse(request)

    assert response.status_code == 200
    update_spy.return_value.update.assert_called_once_with(comment='')
