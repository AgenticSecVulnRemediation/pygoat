import pytest
from django.template import Context, Template


def test_xss_lab_template_escapes_query_by_default():
    """Regression: query must not be rendered with the unsafe |safe filter."""

    # Arrange: simulate attacker-controlled input
    attacker_input = "<script>alert('xss')</script>"

    # Read the updated template from repository path
    with open("introduction/templates/Lab/XSS/xss_lab.html", "r", encoding="utf-8") as f:
        template_source = f.read()

    # Act: render only the affected branch (query provided, company missing)
    rendered = Template(template_source).render(Context({"query": attacker_input}))

    # Assert: the raw script tag must not appear; it should be HTML-escaped
    assert attacker_input not in rendered
    assert "&lt;script&gt;" in rendered
    assert "&lt;/script&gt;" in rendered
