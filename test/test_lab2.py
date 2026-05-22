import pytest
from django.template import Context, Engine


def test_lab2_template_escapes_username_by_default_after_safe_filter_removed():
    """Regression test for template XSS: username must be escaped (no 'safe' filter)."""
    # Arrange: render only the changed line using Django template engine
    template_source = "<h1>Hey {{ username }},</h1>"
    engine = Engine.get_default() if Engine.get_default() is not None else Engine(debug=True)
    template = engine.from_string(template_source)

    # Attempted HTML injection payload
    username = '<img src=x onerror="alert(1)">'  # would execute if marked safe

    # Act
    rendered = template.render(Context({"username": username}))

    # Assert: ensure HTML is escaped and raw payload is not present
    assert "<img" not in rendered
    assert "&lt;img" in rendered
    assert "onerror" in rendered  # still present but escaped
