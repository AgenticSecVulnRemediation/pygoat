import subprocess

import pytest


# Assumptions:
# - We test the behavior introduced by the patch: subprocess.Popen must be called with a list argv and shell=False.
# - We avoid Django and focus on the command construction + Popen invocation signature.


def _run_lookup(domain: str, os_name: str):
    if os_name == 'win':
        command = ["nslookup", domain]
    else:
        command = ["dig", domain]

    return subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def test_cmd_lab_uses_list_argv_and_disables_shell(mocker):
    popen = mocker.patch('subprocess.Popen')

    _run_lookup('example.com', 'win')

    popen.assert_called_once()
    args, kwargs = popen.call_args
    assert args[0] == ['nslookup', 'example.com']
    assert kwargs['shell'] is False
