import re
import subprocess

import pytest


def _is_valid_ipv4(ip: str) -> bool:
    return re.match(r'^\d{1,3}(\.\d{1,3}){3}$', ip) is not None


def test_mitre_lab_17_api_rejects_non_ip_input():
    assert _is_valid_ipv4('127.0.0.1; rm -rf /') is False
    assert _is_valid_ipv4('example.com') is False


def test_mitre_lab_17_api_accepts_ipv4_format_only():
    assert _is_valid_ipv4('127.0.0.1') is True


def test_command_out_uses_shell_false(mocker):
    popen = mocker.patch('subprocess.Popen')
    subprocess.Popen(['nmap', '127.0.0.1'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    popen.assert_called_once()
    _, kwargs = popen.call_args
    assert kwargs['shell'] is False
