import pytest


# Assumption: module path is introduction.views as indicated by file_path.
from introduction.views import xxe_parse


def test_xxe_parse_handles_missing_text_node(monkeypatch):
    """Regression: after fix, missing <text> node should not crash (text becomes empty string)."""

    class DummyBody:
        def decode(self, encoding):
            assert encoding == "utf-8"
            return "<root></root>"

    class DummyRequest:
        body = DummyBody()

    # Avoid touching the database in unit test: comments.objects.filter(...).update(...)
    class DummyQuerySet:
        def update(self, **kwargs):
            # Ensure it updates with empty text when no <text> node exists
            assert kwargs.get("comment") == ""
            return 1

    class DummyCommentsObjects:
        def filter(self, **kwargs):
            assert kwargs.get("id") == 1
            return DummyQuerySet()

    import introduction.views as views

    monkeypatch.setattr(views, "comments", type("C", (), {"objects": DummyCommentsObjects()})())
    monkeypatch.setattr(views, "render", lambda request, template_name: (request, template_name))

    resp = xxe_parse(DummyRequest())
    assert resp[1] == "Lab/XXE/xxe_lab.html"
