import pathlib

import pytest


def test_xss_lab_2_template_no_longer_marks_username_safe():
    template_path = pathlib.Path("introduction/templates/Lab/XSS/xss_lab_2.html")
    if not template_path.exists():
        pytest.skip("template not present in test environment")

    src = template_path.read_text(encoding="utf-8")

    assert "username|safe" not in src
    assert "Hello, {{ username }}" in src
