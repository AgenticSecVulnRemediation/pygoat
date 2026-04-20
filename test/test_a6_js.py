import pathlib

import pytest


def test_a6_js_escapes_html_before_sending_code():
    js_path = pathlib.Path("introduction/static/js/a6.js")
    if not js_path.exists():
        pytest.skip("a6.js not present in test environment")

    src = js_path.read_text(encoding="utf-8")

    assert "function escapeHtml" in src
    assert "var code = escapeHtml" in src
