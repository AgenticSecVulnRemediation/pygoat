import pytest


def test_mitre_lab_17_template_avoids_innerhtml_concat_for_ports():
    """Regression test for DOM XSS: template must not build HTML via innerHTML concatenation."""
    from pathlib import Path

    template_path = Path("introduction/templates/mitre/mitre_lab_17.html")
    content = template_path.read_text(encoding="utf-8")

    assert "output.innerHTML +=" not in content
    assert ".textContent = ports[p]" in content
