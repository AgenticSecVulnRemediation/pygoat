import pytest


def test_xss_lab_2_template_removes_safe_filter():
    """Regression test for PR: ensure the username is no longer marked safe in template."""
    # Arrange / Act
    with open('introduction/templates/Lab/XSS/xss_lab_2.html', 'r', encoding='utf-8') as f:
        template = f.read()

    # Assert
    assert '{{ username|safe }}' not in template
    assert '{{ username }}' in template
