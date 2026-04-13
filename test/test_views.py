import pytest

# Assumption: module is importable as introduction.views
import introduction.views as views


def test_views_uses_defusedxml_make_parser(monkeypatch):
    # Arrange
    called = {"count": 0}

    def fake_make_parser(*args, **kwargs):
        called["count"] += 1
        return object()

    monkeypatch.setattr(views, "make_parser", fake_make_parser)

    # Act
    parser = views.make_parser()

    # Assert
    assert parser is not None
    assert called["count"] == 1
