{#
Assumption: Django template autoescape is enabled by default.
We assert the removal of the "safe" filter in the template by checking the source.
This is a delta/unit-style template test that does not require Django to render.
#}

import pathlib


def test_xss_lab_2_template_does_not_mark_username_safe():
    tpl = pathlib.Path('introduction/templates/Lab/XSS/xss_lab_2.html').read_text(encoding='utf-8')
    assert 'username|safe' not in tpl
    assert '{{ username }}' in tpl
