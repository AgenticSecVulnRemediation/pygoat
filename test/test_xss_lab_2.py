import re


def test_xss_lab_2_template_no_longer_marks_username_safe():
    # Delta: the template removed the |safe filter.
    # This regression test asserts that the raw string "|safe" is not present.
    from pathlib import Path

    template_path = Path('introduction/templates/Lab/XSS/xss_lab_2.html')
    content = template_path.read_text(encoding='utf-8')

    assert re.search(r'\{\{\s*username\s*\|\s*safe\s*\}\}', content) is None
    assert re.search(r'\{\{\s*username\s*\}\}', content) is not None
