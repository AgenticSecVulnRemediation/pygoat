import pytest

# Assumptions:
# - Template file is tracked in repo; delta removes the '|safe' filter.
# - We validate the template no longer contains '|safe' on username interpolation.


def test_xss_lab2_template_does_not_mark_username_safe():
    # This is a lightweight regression guard to ensure the insecure filter isn't reintroduced.
    from pathlib import Path

    path = Path("introduction/templates/Lab/XSS/xss_lab_2.html")
    content = path.read_text(encoding="utf-8")

    assert "{{ username|safe }}" not in content
    assert "{{ username }}" in content
