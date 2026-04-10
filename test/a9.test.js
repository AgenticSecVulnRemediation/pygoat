import pytest


def test_a9_event3_uses_textcontent_not_innerhtml():
    # Regression test: ensure the XSS sink was changed from innerHTML to textContent.
    # We assert on source text to keep this deterministic without a browser DOM.
    from pathlib import Path

    js_path = Path('introduction/static/js/a9.js')
    content = js_path.read_text(encoding='utf-8')

    assert 'li.textContent = data.logs[i]' in content
    assert 'li.innerHTML = data.logs[i]' not in content
