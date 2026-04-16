import pytest

# NOTE: This is a static regression test (file-content assertion) to ensure the XSS fix remains applied.

def test_a8_lab2_template_no_longer_marks_username_safe():
    template_path = "introduction/templates/Lab_2021/A8_software_and_data_integrity_failure/lab2.html"

    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "{{username | safe}}" not in content
    assert "{{username}}" in content
