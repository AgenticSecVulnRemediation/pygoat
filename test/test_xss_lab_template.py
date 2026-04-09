import pytest

# Assumption: Django template file is present in repo; we validate the security fix by asserting
# the unsafe '|safe' filter was removed from the specific line.

def test_xss_lab_template_does_not_use_safe_filter_for_query():
    with open('introduction/templates/Lab/XSS/xss_lab.html', 'r', encoding='utf-8') as f:
        content = f.read()

    assert "query|safe" not in content
    assert "{{ query }}" in content
