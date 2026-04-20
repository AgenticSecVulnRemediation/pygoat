import pathlib

import pytest


def test_template_removed_safe_filter_for_username_output():
    template_path = pathlib.Path(
        "introduction/templates/Lab_2021/A8_software_and_data_integrity_failure/lab2.html"
    )
    if not template_path.exists():
        pytest.skip("template not present in test environment")

    src = template_path.read_text(encoding="utf-8")

    assert "username | safe" not in src
    assert "{{ username }}" in src
