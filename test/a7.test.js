import pytest


def test_a7_js_sanitizes_user_input_before_submit():
    # Regression test: ensure sanitize() is applied to a7_input before form submission.
    from pathlib import Path

    js_path = Path('introduction/static/js/a7.js')
    content = js_path.read_text(encoding='utf-8')

    assert 'function sanitize' in content
    assert "sanitize(document.getElementById('a7_input').value" in content
