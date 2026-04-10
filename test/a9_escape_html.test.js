import pytest


def test_a9_js_escapes_html_special_chars_for_inputs():
    # Regression test: ensure escapeHtml() is used for user-controlled inputs.
    from pathlib import Path

    js_path = Path('introduction/static/js/a9.js')
    content = js_path.read_text(encoding='utf-8')

    assert 'function escapeHtml' in content
    assert "var log_code = escapeHtml(document.getElementById('a9_log').value)" in content
    assert "var target_code = escapeHtml(document.getElementById('a9_api').value)" in content
