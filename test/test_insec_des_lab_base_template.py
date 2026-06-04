import pytest


def test_base_html_validates_localstorage_theme_value_to_light_or_dark():
    """Regression test: only 'light'/'dark' should be honored from localStorage."""
    from pathlib import Path

    template_path = Path("dockerized_labs/insec_des_lab/templates/base.html")
    content = template_path.read_text(encoding="utf-8")

    # Ensure the sanitization guard is present
    assert "savedTheme !== 'dark'" in content and "savedTheme !== 'light'" in content
    assert "savedTheme = 'light'" in content
