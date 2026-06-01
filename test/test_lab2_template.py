{#
Delta test note: this repo may not have Django template unit test harness configured.
This test asserts the security intent of removing the `safe` filter by checking the template source.
#}

import pathlib


def test_lab2_template_no_longer_marks_username_safe():
    template_path = pathlib.Path(__file__).resolve().parents[1] / "introduction" / "templates" / "Lab_2021" / "A8_software_and_data_integrity_failure" / "lab2.html"
    content = template_path.read_text(encoding="utf-8")

    assert "username | safe" not in content
    assert "{{ username }}" in content
