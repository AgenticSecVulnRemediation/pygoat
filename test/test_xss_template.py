import re


def test_xss_lab_template_does_not_use_safe_filter_anymore():
    """Delta test: ensure query is not rendered with the |safe filter (prevents reflected XSS)."""

    # Read the template file relative to repo root during test execution.
    # This keeps the test focused on the exact regression: removal of '|safe'.
    with open("introduction/templates/Lab/XSS/xss_lab.html", "r", encoding="utf-8") as f:
        content = f.read()

    assert "query|safe" not in content

    # Also ensure query is still present (feature retained)
    assert re.search(r"\{\{\s*query\s*\}\}", content) is not None
