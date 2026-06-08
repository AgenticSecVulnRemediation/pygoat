import os

import pytest
from django.test import RequestFactory

from introduction.views import cmd_lab


def test_cmd_lab_uses_subprocess_without_shell_and_argv_list(mocker):
    rf = RequestFactory()
    request = rf.post('/cmd/lab', data={'domain': 'example.com; rm -rf /', 'os': 'linux'})
    request.user = type('U', (), {'is_authenticated': True})()

    # Avoid template rendering
    mocker.patch('introduction.views.render', side_effect=lambda _r, _t, ctx=None: ctx)

    process_mock = mocker.Mock()
    process_mock.communicate.return_value = (b'out', b'')
    popen_spy = mocker.patch('introduction.views.subprocess.Popen', return_value=process_mock)

    ctx = cmd_lab(request)

    popen_spy.assert_called_once()
    called_args, called_kwargs = popen_spy.call_args
    assert called_args[0] == ['dig', 'example.com; rm -rf /']
    # shell should not be passed as True; best check is that it is absent or False
    assert called_kwargs.get('shell', False) is False


def test_cmd_lab_windows_branch_uses_nslookup_argv_list(mocker):
    rf = RequestFactory()
    request = rf.post('/cmd/lab', data={'domain': 'example.com', 'os': 'win'})
    request.user = type('U', (), {'is_authenticated': True})()

    mocker.patch('introduction.views.render', side_effect=lambda _r, _t, ctx=None: ctx)

    process_mock = mocker.Mock()
    process_mock.communicate.return_value = (b'out', b'')
    popen_spy = mocker.patch('introduction.views.subprocess.Popen', return_value=process_mock)

    cmd_lab(request)

    called_args, _ = popen_spy.call_args
    assert called_args[0] == ['nslookup', 'example.com']
