import pytest


def test_a8_lab2_template_does_not_use_safe_filter_for_username():
    """Regression test for XSS: username must not be rendered with the safe filter."""
    from pathlib import Path

    template_path = Path(
        "introduction/templates/Lab_2021/A8_software_and_data_integrity_failure/lab2.html"
    )
    content = template_path.read_text(encoding="utf-8")

    assert "username | safe" not in content
    assert "username|safe" not in content
    assert "{{username}}" in content or "{{ username }}" in content
