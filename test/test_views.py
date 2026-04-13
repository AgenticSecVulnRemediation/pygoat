import types
import pytest


# Delta covered: xxe_parse no longer enables external general entities and no longer
# parses via pulldom; it now uses defusedxml.minidom.parseString and safe node access.

def test_xxe_parse_ignores_external_entities_and_returns_empty_text(mocker):
    from introduction import views

    # Arrange: mock the ORM update call so no DB is required
    update_mock = mocker.Mock(return_value=1)
    mocker.patch.object(views.comments, "objects", mocker.Mock(filter=mocker.Mock(return_value=mocker.Mock(update=update_mock))))

    class DummyRequest:
        def __init__(self, body: bytes):
            self.body = body

    # Payload includes external entity; defusedxml should prevent expansion and parsing should fall back to ""
    xml = b"""<?xml version='1.0'?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM 'file:///etc/passwd'> ]>
<root><text>&xxe;</text></root>"""

    req = DummyRequest(xml)

    # Act
    views.xxe_parse(req)

    # Assert
    update_mock.assert_called_once()
    assert update_mock.call_args.kwargs.get("comment") == ""
