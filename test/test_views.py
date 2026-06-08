import pytest
from django.http import HttpResponse

# These tests validate security hardening in introduction.views.cmd_lab()
# and ensure command injection attempts are rejected.


class _User:
    is_authenticated = True


class _Request:
    def __init__(self, domain: str, os_value: str = 'win'):
        self.user = _User()
        self.method = 'POST'
        self.POST = {'domain': domain, 'os': os_value}


def test_cmd_lab_rejects_domain_with_shell_metacharacters(mocker):
    """Previously, shell=True and string formatting allowed injection.

    After the fix, domains must match ^[a-zA-Z0-9.-]+$ and invalid input returns HTTP 400.
    """
    from introduction import views

    # Ensure no subprocess execution occurs on invalid input
    popen_spy = mocker.patch('introduction.views.subprocess.Popen')

    req = _Request(domain='example.com; cat /etc/passwd')
    resp = views.cmd_lab(req)

    assert isinstance(resp, HttpResponse)
    assert resp.status_code == 400
    assert b'Invalid domain' in resp.content
    popen_spy.assert_not_called()


def test_cmd_lab_allows_valid_domain_and_uses_shell_false(mocker):
    """Valid domains should be executed with shell=False and argv-list commands."""
    from introduction import views

    proc = mocker.Mock()
    proc.communicate.return_value = (b'OK', b'')
    popen_mock = mocker.patch('introduction.views.subprocess.Popen', return_value=proc)

    req = _Request(domain='example.com', os_value='win')
    resp = views.cmd_lab(req)

    # Rendered response (template) is a Django HttpResponse
    assert isinstance(resp, HttpResponse)
    assert resp.status_code == 200

    popen_mock.assert_called_once()
    args, kwargs = popen_mock.call_args
    # first arg should be argv list: ['nslookup', 'example.com']
    assert args[0] == ['nslookup', 'example.com']
    assert kwargs.get('shell') is False
