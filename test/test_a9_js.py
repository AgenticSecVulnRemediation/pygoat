import pathlib

import pytest


def test_a9_js_sanitizes_inputs_with_dompurify():
    js_path = pathlib.Path("introduction/static/js/a9.js")
    if not js_path.exists():
        pytest.skip("a9.js not present in test environment")

    src = js_path.read_text(encoding="utf-8")

    assert "import DOMPurify" in src
    assert "DOMPurify.sanitize" in src
    assert "var log_code = DOMPurify.sanitize" in src
    assert "var target_code = DOMPurify.sanitize" in src
