import pytest


# Assumptions:
# - pytest is used.
# - We can import the Django view module directly.


def _make_authenticated_request(body_bytes=b"<root/>"):
    class _User:
        is_authenticated = True

    class _Req:
        user = _User()
        method = "POST"
        body = body_bytes

    return _Req()


def test_xxe_parse_uses_defusedxml_pulldom_parser(mocker):
    """Regression: xxe_parse should use defusedxml.pulldom.parseString instead of xml.dom.pulldom.parseString."""
    from introduction import views

    # Arrange
    # We stub parseString from the module to ensure it's called. Since the patch changes the import
    # location, we verify that views.parseString refers to defusedxml implementation by checking module.
    assert views.parseString.__module__.startswith("defusedxml"), (
        f"Expected defusedxml parseString, got {views.parseString.__module__}"
    )

    # Also ensure the vulnerable stdlib parser is not used via that symbol.
    # (We don't import stdlib parseString here to avoid reintroducing it.)

    # Stub out downstream xml processing to avoid full XML parsing complexity.
    # parseString returns an object iterable over events/nodes; easiest is to patch it.
    fake_doc = [(views.START_ELEMENT, type("N", (), {"tagName": "text", "toxml": lambda self: "<text>ok</text>"})())]
    mocker.patch.object(views, "parseString", return_value=fake_doc)
    mocker.patch.object(views, "render", return_value="RESPONSE")
    mocker.patch.object(views.comments.objects, "filter", return_value=type("Q", (), {"update": lambda self, **kw: 1})())

    req = _make_authenticated_request(b"<text>ok</text>")

    # Act
    resp = views.xxe_parse(req)

    # Assert
    assert resp == "RESPONSE"
