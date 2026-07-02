import pathlib


def test_lab2_template_does_not_mark_username_safe():
    tpl = pathlib.Path(
        'introduction/templates/Lab_2021/A8_software_and_data_integrity_failure/lab2.html'
    ).read_text(encoding='utf-8')

    assert 'username | safe' not in tpl
    assert 'username|safe' not in tpl
    assert 'Hey {{ username }}' in tpl
