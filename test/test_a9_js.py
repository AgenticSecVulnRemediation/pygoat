import pytest


def test_a9_logs_use_text_content_not_inner_html():
    """Regression: avoid DOM XSS by not assigning untrusted logs to innerHTML."""
    from pathlib import Path

    js_path = Path("introduction/static/js/a9.js")
    content = js_path.read_text(encoding="utf-8")

    assert "li.textContent" in content
    assert "li.innerHTML = data.logs[i]" not in content
