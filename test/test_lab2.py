import pytest


# Delta covered: template no longer uses the Django "safe" filter for username.
# We enforce that the "safe" filter is absent so user-supplied HTML is escaped by default.

def test_lab2_template_does_not_mark_username_as_safe():
    from pathlib import Path

    template_path = Path(
        "introduction/templates/Lab_2021/A8_software_and_data_integrity_failure/lab2.html"
    )
    content = template_path.read_text(encoding="utf-8")

    assert "username | safe" not in content
    # ensure username is still rendered
    assert "{{ username" in content
