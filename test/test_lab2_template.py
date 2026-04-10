import pytest


def test_a8_lab2_template_no_longer_marks_username_safe():
    # Delta test: ensure the security fix removed the `|safe` filter.
    from pathlib import Path

    template_path = Path('introduction/templates/Lab_2021/A8_software_and_data_integrity_failure/lab2.html')
    content = template_path.read_text(encoding='utf-8')

    assert '{{username | safe}}' not in content
    assert '{{ username }}' in content
