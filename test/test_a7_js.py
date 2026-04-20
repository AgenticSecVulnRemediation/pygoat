import types
from unittest.mock import MagicMock

import pytest


def test_a7_js_uses_dompurify_sanitize_for_user_input():
    import pathlib

    js_path = pathlib.Path("introduction/static/js/a7.js")
    if not js_path.exists():
        pytest.skip("a7.js not present in test environment")

    src = js_path.read_text(encoding="utf-8")

    assert "DOMPurify" in src
    assert "DOMPurify.sanitize" in src
    assert "document.getElementById('a7_input').value" in src
