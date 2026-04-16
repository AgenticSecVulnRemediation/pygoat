import types

import pytest


@pytest.mark.django_db
def test_software_and_data_integrity_failure_lab2_escapes_username(mocker):
    """Delta behavior: request.GET.get default + django.utils.html.escape applied."""

    from introduction import views

    # Mock render to observe context without depending on templates
    render_spy = mocker.patch.object(views, 'render', autospec=True, return_value=types.SimpleNamespace(status_code=200))

    request = types.SimpleNamespace(
        method='GET',
        user=types.SimpleNamespace(is_authenticated=True),
        GET={'username': '<img src=x onerror=alert(1)>'},
    )

    views.software_and_data_integrity_failure_lab2(request)

    _, _, template, context = render_spy.mock.calls[0][0]
    assert context['username'] == '&lt;img src=x onerror=alert(1)&gt;'
