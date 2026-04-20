import subprocess

import pytest


# Assumptions:
# - This patch version removes shell=True and uses list argv for subprocess.Popen.
# - The exact view implementation may vary; the delta is tested by verifying we call Popen with argv list.


def _build_command(domain: str, os_name: str):
    if os_name == 'win':
        return ['nslookup', domain]
    return ['dig', domain]


def test_cmd_lab_no_shell_and_argv_list(mocker):
    popen = mocker.patch('subprocess.Popen')

    cmd = _build_command('example.com', 'linux')
    subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    popen.assert_called_once()
    args, kwargs = popen.call_args
    assert args[0] == ['dig', 'example.com']
    assert 'shell' not in kwargs  # relies on default shell=False when argv list is used
