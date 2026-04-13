import pytest


# Assumption: project does not expose a testable JS module for the inline script in base.html.
# This unit test asserts the security-relevant delta: use of textContent (not innerHTML)
# in the updated template to prevent DOM XSS.

def test_base_template_uses_textcontent_not_innerhtml_for_theme_toggle():
    from pathlib import Path

    template_path = Path("dockerized_labs/insec_des_lab/templates/base.html")
    content = template_path.read_text(encoding="utf-8")

    assert "themeToggle.textContent" in content
    assert "themeToggle.innerHTML" not in content
