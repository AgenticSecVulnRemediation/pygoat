import pytest


def test_base_template_validates_theme_from_local_storage():
    """Regression: only allow known themes to be applied (prevents DOM clobbering/injection vectors)."""
    from pathlib import Path

    template_path = Path("dockerized_labs/insec_des_lab/templates/base.html")
    content = template_path.read_text(encoding="utf-8")

    assert "const validThemes" in content
    assert "validThemes.includes(savedTheme)" in content
