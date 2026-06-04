import re

import pytest


def test_xss_lab2_template_no_longer_marks_username_safe():
    """Regression test for stored/reflected XSS: username must not be rendered with the safe filter."""
    from pathlib import Path

    template_path = Path("introduction/templates/Lab/XSS/xss_lab_2.html")
    content = template_path.read_text(encoding="utf-8")

    assert "username|safe" not in content
    assert re.search(r"\{\{\s*username\s*\}\}", content)
