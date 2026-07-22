import types


def test_xss_lab_2_template_does_not_mark_username_safe_allows_autoescape():
    # This is a structural regression test ensuring the dangerous `|safe` filter
    # is not present anymore, preventing reflected XSS.
    from introduction.templates.Lab.XSS import xss_lab_2  # type: ignore

    # Django templates aren't importable as modules in typical setups.
    # Instead, keep the assertion at the source-string level via pkgutil.
    import pkgutil

    data = pkgutil.get_data('introduction', 'templates/Lab/XSS/xss_lab_2.html')
    assert data is not None
    text = data.decode('utf-8')

    assert '{{ username|safe }}' not in text
    assert '{{ username }}' in text
