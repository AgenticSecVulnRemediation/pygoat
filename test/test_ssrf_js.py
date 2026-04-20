import pathlib

import pytest


def test_ssrf_js_uses_dompurify_for_html_code():
    js_path = pathlib.Path("introduction/static/Lab/ssrf.js")
    if not js_path.exists():
        pytest.skip("ssrf.js not present in test environment")

    src = js_path.read_text(encoding="utf-8")

    assert "import DOMPurify" in src
    assert "DOMPurify.sanitize" in src
    assert "var html_code = DOMPurify.sanitize" in src
