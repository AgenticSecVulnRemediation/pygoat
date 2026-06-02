import pytest


def test_xss_lab_2_template_no_safe_filter_applied():
    """Regression: username output must be autoescaped (no |safe)."""
    # The PR changes the template to remove the `|safe` filter.
    # This unit test asserts the template content does not reintroduce it.
    from pathlib import Path

    template_path = Path("introduction/templates/Lab/XSS/xss_lab_2.html")
    content = template_path.read_text(encoding="utf-8")

    assert "{{ username|safe }}" not in content
    assert "{{ username }}" in content
