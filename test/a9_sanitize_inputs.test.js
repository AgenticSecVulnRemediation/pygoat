import pytest


def test_a9_js_sanitizes_log_and_api_code_inputs():
    # Regression test: ensure user-controlled inputs are sanitized before being appended to FormData.
    from pathlib import Path

    js_path = Path('introduction/static/js/a9.js')
    content = js_path.read_text(encoding='utf-8')

    assert 'function sanitize' in content
    assert 'var log_code = sanitize(rawLogCode)' in content
    assert 'var target_code = sanitize(rawTargetCode)' in content
