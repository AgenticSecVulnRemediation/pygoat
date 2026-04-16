import types

import pytest


@pytest.mark.django_db
def test_mitre_lab_17_api_rejects_invalid_ip_and_does_not_execute_subprocess(mocker):
    """Assumptions:
    - introduction.mitre.mitre_lab_17_api is imported in Django urls and can be called directly.
    - We can call the view with a minimal request object that has method and POST.
    Delta behavior:
    - Reject invalid IP and avoid running nmap via shell/command execution.
    """

    from introduction import mitre as mitre_module

    popen_spy = mocker.patch.object(mitre_module.subprocess, 'Popen')

    request = types.SimpleNamespace(method='POST', POST={'ip': '127.0.0.1; rm -rf /'})

    response = mitre_module.mitre_lab_17_api(request)

    assert response.status_code == 400
    popen_spy.assert_not_called()
