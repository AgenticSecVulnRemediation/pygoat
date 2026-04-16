import pytest

# NOTE: This is a static regression test (file-content assertion) to ensure theme validation remains applied.

def test_insec_des_base_template_sanitizes_theme_value():
    template_path = "dockerized_labs/insec_des_lab/templates/base.html"

    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "const safeTheme" in content
    assert "(savedTheme === 'dark' || savedTheme === 'light')" in content
