import pytest


def test_xss_lab_2_template_no_longer_marks_username_safe():
    # Delta test: ensure the security fix removed the `|safe` filter.
    # This prevents user-controlled HTML/JS from being rendered unescaped.
    from pathlib import Path

    template_path = Path('introduction/templates/Lab/XSS/xss_lab_2.html')
    content = template_path.read_text(encoding='utf-8')

    assert '{{ username|safe }}' not in content
    assert '{{ username }}' in content
