import pytest


def test_base_template_theme_validation_only_allows_light_or_dark():
    """Delta test: ensure unsafe localStorage theme is validated before setAttribute."""

    # This change is in an HTML template with embedded JS.
    # Assert that validation logic exists and setAttribute uses validated theme.
    with open("dockerized_labs/insec_des_lab/templates/base.html", "r", encoding="utf-8") as f:
        content = f.read()

    assert "const validTheme" in content
    assert "(savedTheme === 'light' || savedTheme === 'dark')" in content
    assert "html.setAttribute('data-theme', validTheme)" in content
    # Previous vulnerable behavior would set the attribute using savedTheme directly
    assert "html.setAttribute('data-theme', savedTheme)" not in content
