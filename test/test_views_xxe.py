from types import SimpleNamespace

import pytest

# We mock xml parsing entry point (parseString) to capture the configured parser.
import introduction.views as views


def _fake_authenticated_request(body: bytes):
    return SimpleNamespace(
        user=SimpleNamespace(is_authenticated=True),
        body=body,
    )


def test_xxe_parse_disables_external_general_entities(monkeypatch):
    """Regression for XXE fix: parser must have feature_external_ges disabled."""
    captured = {}

    def fake_parse_string(_xml_text, parser=None):
        captured["parser"] = parser
        # Return an iterable compatible with: for event, node in doc:
        class _Doc(list):
            def __iter__(self):
                return iter([])

        return _Doc()

    monkeypatch.setattr(views, "parseString", fake_parse_string)

    # Act
    views.xxe_parse(_fake_authenticated_request(b"<root></root>"))

    # Assert: feature_external_ges should have been set to False.
    parser = captured["parser"]
    assert parser is not None
    assert getattr(parser, "getFeature")(views.feature_external_ges) is False
