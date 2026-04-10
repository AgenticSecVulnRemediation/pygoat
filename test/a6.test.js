import pytest


def test_a6_js_sanitizes_code_with_dompurify():
    # Regression test: ensure DOMPurify.sanitize is used before sending code.
    from pathlib import Path

    js_path = Path('introduction/static/js/a6.js')
    content = js_path.read_text(encoding='utf-8')

    assert 'DOMPurify.sanitize' in content
    assert 'formdata.append("code", sanitizedCode)' in content
