import pytest
from django.http import HttpRequest

# Assumption: Django app module path is introduction.views
from introduction import views


class _DummyUser:
    def __init__(self, authenticated: bool = True):
        self.is_authenticated = authenticated


class _DummyCommentsManager:
    def __init__(self):
        self.updated_kwargs = None

    def filter(self, **kwargs):
        return self

    def update(self, **kwargs):
        self.updated_kwargs = kwargs
        return 1


def _make_request(body: bytes) -> HttpRequest:
    req = HttpRequest()
    req.method = "POST"
    req.user = _DummyUser(True)
    req._body = body
    return req


def test_xxe_parse_rejects_empty_body_returns_400(monkeypatch):
    # Arrange
    request = _make_request(b"")

    # Act
    response = views.xxe_parse(request)

    # Assert
    assert response.status_code == 400
    assert b"Empty XML input" in response.content


def test_xxe_parse_rejects_missing_text_element_returns_400(monkeypatch):
    # Arrange
    request = _make_request(b"<root><nope>hi</nope></root>")

    # Patch model manager to ensure no update is attempted
    dummy_manager = _DummyCommentsManager()
    monkeypatch.setattr(views, "comments", type("C", (), {"objects": dummy_manager}))

    # Act
    response = views.xxe_parse(request)

    # Assert
    assert response.status_code == 400
    assert b"required text element" in response.content
    assert dummy_manager.updated_kwargs is None
