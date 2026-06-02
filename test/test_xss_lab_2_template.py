import pytest


def test_xss_lab2_template_no_longer_marks_username_as_safe():
    # This patch removes the '|safe' filter, reducing XSS exposure.
    # We assert the template no longer contains the unsafe filter.
    template_path = "introduction/templates/Lab/XSS/xss_lab_2.html"

    # Read from filesystem; in most Django projects templates are part of repo.
    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "{{ username|safe }}" not in content
    assert "{{ username }}" in content
