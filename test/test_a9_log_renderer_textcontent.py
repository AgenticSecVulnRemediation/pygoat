import pytest


def test_a9_log_renderer_uses_textcontent_not_innerhtml():
    """Delta test: ensure XSS fix uses textContent rather than innerHTML when rendering logs."""

    # The fix is in a static JS file. We can't execute a browser here reliably,
    # so we assert the secure primitive is present and the unsafe one is absent.
    with open("introduction/static/js/a9.js", "r", encoding="utf-8") as f:
        content = f.read()

    assert "li.textContent = data.logs[i]" in content
    assert "li.innerHTML = data.logs[i]" not in content
