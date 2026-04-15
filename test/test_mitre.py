import types

import pytest

from introduction import mitre


def test_mitre_lab_17_api_rejects_invalid_ip(mocker):
    request = types.SimpleNamespace(method="POST", POST={"ip": "1.2.3.4; rm -rf /"})

    command_out = mocker.patch.object(mitre, "command_out")

    resp = mitre.mitre_lab_17_api(request)

    assert resp.status_code == 400
    command_out.assert_not_called()


def test_command_out_uses_shell_false_and_argv(mocker):
    popen = mocker.patch.object(mitre.subprocess, "Popen")
    popen.return_value.communicate.return_value = (b"", b"")

    mitre.command_out(["nmap", "127.0.0.1"])

    args, kwargs = popen.call_args
    assert args[0] == ["nmap", "127.0.0.1"]
    assert kwargs.get("shell") is False
