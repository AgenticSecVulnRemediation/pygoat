# Assumptions:
# - Django project uses pytest with pytest-django enabled.
# - Template auto-escaping is enabled by default.

from django.template import Context, Template


def test_xss_lab_template_escapes_query_in_not_found_message():
    """Regression test for XSS: `query` should not be rendered with `|safe`."""

    tpl = Template(
        "{% if company %}ok{% elif query %}"
        "<h3> The company '{{query}}' You searched for is not Part of FAANG</h3>"
        "{% endif %}"
    )

    payload = "<svg/onload=alert(1)>"
    rendered = tpl.render(Context({"company": None, "query": payload}))

    assert payload not in rendered
    assert "&lt;svg" in rendered
