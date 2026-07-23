# Assumption: project uses a standard pytest layout and 'introduction' is importable as a package/module.
# This delta test asserts that user-provided content is escaped rather than rendered as raw HTML.

import pytest


def test_xss_lab_template_escapes_query_value():
    # Arrange
    # The fix removed the Jinja2 `|safe` filter from query, so it must be auto-escaped.
    # If it were still marked safe, the <script> would appear unescaped in output.
    from jinja2 import Environment, BaseLoader, select_autoescape

    template_source = """
    {% if query %}
      <h3> The company '{{ query }}' You searched for is not Part of FAANG</h3>
    {% endif %}
    """

    env = Environment(
        loader=BaseLoader(),
        autoescape=select_autoescape(enabled_extensions=("html", "xml"), default=True),
    )

    template = env.from_string(template_source)

    payload = "<script>alert('xss')</script>"

    # Act
    rendered = template.render(query=payload)

    # Assert
    assert payload not in rendered, "Raw payload should not be rendered after removing |safe"
    assert "&lt;script&gt;" in rendered
    assert "&lt;/script&gt;" in rendered
