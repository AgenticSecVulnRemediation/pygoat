import pytest

try:
    from django.template import Context, Engine
except Exception:  # pragma: no cover
    pytest.skip("Django not available in test environment", allow_module_level=True)


def test_xss_lab_2_escapes_username_output():
    # Delta: switched from |safe to |escape
    template_source = "<p>Hello, {{ username|escape }}</p>"
    tpl = Engine.get_default().from_string(template_source)

    rendered = tpl.render(Context({"username": "<script>alert(1)</script>"}))

    assert "<script>" not in rendered
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in rendered
