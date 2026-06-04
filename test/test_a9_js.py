import pytest


def test_a9_js_uses_textContent_instead_of_innerHTML_to_prevent_xss():
    """Regression test: appending logs must use textContent to avoid DOM XSS."""
    from pathlib import Path

    js_path = Path("introduction/static/js/a9.js")
    content = js_path.read_text(encoding="utf-8")

    assert "li.textContent = data.logs[i]" in content
    assert "li.innerHTML = data.logs[i]" not in content
