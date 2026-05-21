import pytest


def test_lab2_username_is_escaped_by_default_and_not_marked_safe():
    """Regression test: template must not use the |safe filter for untrusted username."""
    # Arrange
    template_content = (
        "{% if success %}<h1>Hey {{username}},</h1>{% endif %}"
    )

    from django.template import Context, Template

    tpl = Template(template_content)

    # Act
    rendered = tpl.render(Context({"success": True, "username": "<script>alert(1)</script>"}))

    # Assert: autoescape should escape script tags
    assert "<script>" not in rendered
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in rendered
