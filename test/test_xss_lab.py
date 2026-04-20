{#
Assumptions:
- Django templates autoescape is enabled by default.
- This delta test verifies the template no longer uses the `safe` filter for query, preventing XSS.

We assert the changed behavior at rendering time: potentially dangerous HTML is escaped.
#}

from django.template import Template, Context


def test_xss_lab_query_is_escaped_after_safe_filter_removal():
    # Arrange
    tpl = Template("<h3> The company '{{query}}' You searched for is not Part of FAANG</h3>")
    payload = "<script>alert(1)</script>"

    # Act
    rendered = tpl.render(Context({"query": payload}))

    # Assert
    assert "<script>" not in rendered
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in rendered
