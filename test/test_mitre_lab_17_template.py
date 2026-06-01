import pytest


def test_mitre_lab_17_template_no_longer_builds_html_with_innerhtml():
    """Delta: template now uses DOM createElement+textContent rather than innerHTML concatenation."""
    from pathlib import Path

    template_path = Path(__file__).resolve().parents[1] / "introduction" / "templates" / "mitre" / "mitre_lab_17.html"
    content = template_path.read_text(encoding="utf-8")

    assert "output.innerHTML +=" not in content
    assert "textContent" in content
