import pytest


def test_mitre_lab_17_template_escapes_ports_output():
    """Regression: JS should escape ports before injecting into innerHTML."""
    from pathlib import Path

    template_path = Path("introduction/templates/mitre/mitre_lab_17.html")
    content = template_path.read_text(encoding="utf-8")

    assert "function escapeHTML" in content
    assert "escapeHTML(ports[p])" in content
    # Previously vulnerable pattern
    assert "output.innerHTML += \"<span>\" + ports[p]" not in content
