import types
from unittest.mock import MagicMock

import pytest

# Assumption: Django app module path is "introduction" and xxe_parse is importable from introduction.views
from introduction.views import xxe_parse


def test_xxe_parse_disables_external_general_entities(monkeypatch):
    # Arrange: replace make_parser with spy parser to capture setFeature calls
    parser = MagicMock()

    make_parser_spy = MagicMock(return_value=parser)
    monkeypatch.setattr("introduction.views.make_parser", make_parser_spy)

    # parseString is called; patch it to avoid real XML parsing
    doc_iter = []
    monkeypatch.setattr("introduction.views.parseString", MagicMock(return_value=doc_iter))

    request = types.SimpleNamespace()
    request.user = types.SimpleNamespace(is_authenticated=True)
    request.body = b"<root></root>"

    # Act
    xxe_parse(request)

    # Assert
    make_parser_spy.assert_called_once()
    # Critical security behavior: disable external general entities
    parser.setFeature.assert_any_call(
        monkeypatch.getattr("introduction.views", "feature_external_ges"), False
    )
