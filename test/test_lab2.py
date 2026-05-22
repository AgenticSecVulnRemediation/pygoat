import pytest
from django.template import Context, Template


def test_lab2_template_escapes_username_by_default():
    # Arrange: template behavior after fix should not use the `safe` filter for username
    tmpl = Template("<h1>Hey {{ username }},</h1>")

    # Act: render with a value that would become XSS if not escaped
    rendered = tmpl.render(Context({"username": "<script>alert(1)</script>"}))

    # Assert: ensure output is escaped (Django auto-escaping) and raw script is not present
    assert "<script>alert(1)</script>" not in rendered
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in rendered
