import pytest
from django.test import RequestFactory

from introduction import mitre


def test_mitre_lab_17_api_rejects_invalid_ip_returns_400(mocker):
    rf = RequestFactory()
    request = rf.post('/mitre/17/lab/api', data={'ip': '127.0.0.1; rm -rf /'})

    # Ensure we don't execute any command on invalid input
    popen_spy = mocker.patch('subprocess.Popen', autospec=True)

    response = mitre.mitre_lab_17_api(request)

    assert response.status_code == 400
    popen_spy.assert_not_called()


def test_mitre_lab_17_api_uses_shell_false_and_argv_list(mocker):
    rf = RequestFactory()
    request = rf.post('/mitre/17/lab/api', data={'ip': '127.0.0.1'})

    process_mock = mocker.Mock()
    process_mock.communicate.return_value = (b'STATE SERVICE\n\n22/tcp open ssh\n', b'')

    popen_spy = mocker.patch('subprocess.Popen', return_value=process_mock)

    response = mitre.mitre_lab_17_api(request)

    assert response.status_code == 200
    popen_spy.assert_called_once()

    called_args, called_kwargs = popen_spy.call_args
    assert called_args[0] == ['nmap', '127.0.0.1']
    assert called_kwargs.get('shell') is False
