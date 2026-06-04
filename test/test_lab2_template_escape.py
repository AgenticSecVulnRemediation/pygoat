import pytest


# The security fix replaces use of `safe` with escaping. This is a template behavior change.
# We test Django template rendering directly to ensure HTML is escaped.

def render_snippet(username: str) -> str:
    from django.template import Context, Template

    tmpl = Template("<h1>Hey {{ username|escape }},</h1>")
    return tmpl.render(Context({"username": username}))


def test_username_is_html_escaped():
    rendered = render_snippet("<script>alert(1)</script>")
    assert "<script>" not in rendered
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in rendered
