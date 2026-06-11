import json
import subprocess

import pytest


class _FakeRequest:
    def __init__(self, ip: str):
        self.method = "POST"
        self.POST = {"ip": ip}


def test_mitre_lab_17_api_uses_arg_list_not_shell_command_string(mocker):
    """Regression test for command injection hardening.

    Patch changed:
      - command from "nmap " + ip -> ['nmap', ip]
      - subprocess.Popen(shell=True, ...) -> subprocess.Popen(...)

    Ensure Popen is called with a list argv and without shell=True.
    """

    from introduction import mitre

    popen_mock = mocker.patch.object(subprocess, "Popen", autospec=True)
    popen_mock.return_value.communicate.return_value = (b"STATE SERVICE\n\n80/tcp open http\n", b"")

    request = _FakeRequest("127.0.0.1")

    # Avoid brittle regex parsing behavior by stubbing re.findall to return a safe match.
    mocker.patch.object(mitre.re, "findall", return_value=["STATE SERVICE\n\n80/tcp open http\n"]) 

    response = mitre.mitre_lab_17_api(request)

    assert getattr(response, "status_code", None) == 200

    # Assert subprocess args
    assert popen_mock.call_count == 1
    called_command = popen_mock.call_args.args[0]
    assert called_command == ["nmap", "127.0.0.1"]

    assert popen_mock.call_args.kwargs.get("shell") is None

    payload = json.loads(getattr(response, "content", b"").decode("utf-8"))
    assert "ports" in payload
