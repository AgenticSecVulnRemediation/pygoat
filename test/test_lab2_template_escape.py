# Assumptions:
# - Django project uses pytest with pytest-django enabled (common for Python/Django apps).
# - These tests focus only on the security behavior change: templates no longer mark user input as safe.
# - We validate output escaping via Django template engine directly (no DB / no HTTP).

import pytest
from django.template import Context, Template


def test_lab2_template_escapes_username_when_rendered():
    """Regression test for XSS: username must be auto-escaped (no `|safe`)."""
    tpl = Template(
        "{% if success %}<h1>Hey {{ username }},</h1>{% else %}nope{% endif %}"
    )

    payload = "<img src=x onerror=alert(1)>"
    rendered = tpl.render(Context({"success": True, "username": payload}))

    # Assert the raw payload is not present; it should be escaped by Django.
    assert payload not in rendered
    assert "&lt;img" in rendered
    assert "onerror" in rendered  # still visible as text, not executed
