import types

import pytest


# NOTE:
# Delta test for introduction/views.py XXE hardening:
# - switch to defusedxml parsers
# - external general entities disabled (feature_external_ges=False)
# We assert that the parser feature is set to False.


def _import_views_module():
    try:
        from introduction import views
        return views
    except Exception as e:
        pytest.skip(f"Unable to import introduction.views (likely missing Django settings in unit-test env): {e}")


def _fake_request(body: bytes, authenticated=True):
    user = types.SimpleNamespace(is_authenticated=authenticated)
    return types.SimpleNamespace(user=user, body=body)


def test_xxe_parse_disables_external_general_entities(mocker):
    views = _import_views_module()

    parser = mocker.Mock()
    make_parser = mocker.patch.object(views, 'make_parser', autospec=True, return_value=parser)

    # Arrange: parseString returns an iterable of events; keep it minimal.
    def _fake_doc_iter():
        # Ensure code can set `text` by providing a START_ELEMENT with tagName 'text'
        node = types.SimpleNamespace(tagName='text', toxml=lambda: '<text>hello</text>')
        yield (views.START_ELEMENT, node)

    doc = _fake_doc_iter()
    parse_string = mocker.patch.object(views, 'parseString', autospec=True, return_value=doc)

    # Avoid DB update + template rendering.
    mocker.patch.object(views.comments.objects, 'filter', autospec=True, return_value=mocker.Mock(update=mocker.Mock()))
    mocker.patch.object(views, 'render', autospec=True, return_value={'ok': True})

    req = _fake_request(b'<root><text>hello</text></root>')

    # Act
    views.xxe_parse(req)

    # Assert
    make_parser.assert_called_once()
    parser.setFeature.assert_called_once_with(views.feature_external_ges, False)
    parse_string.assert_called_once()
