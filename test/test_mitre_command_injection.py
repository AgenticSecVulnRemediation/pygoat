import re
import subprocess

import pytest


# Import the module under test
from introduction import mitre


def test_command_out_does_not_invoke_shell_and_passes_argv_list(mocker):
    """Regression test for command injection fix: command_out must not use shell=True."""

    popen_mock = mocker.patch.object(subprocess, "Popen", autospec=True)

    argv = ["nmap", "127.0.0.1"]
    mitre.command_out(argv)

    # Ensure shell kwarg is not set to True anymore and argv list passed as first arg.
    assert popen_mock.call_count == 1
    called_args, called_kwargs = popen_mock.call_args
    assert called_args[0] == argv
    assert called_kwargs.get("shell", False) is False


def test_mitre_lab_17_api_builds_argv_list_from_ip(mocker):
    """Delta test: mitre_lab_17_api should build ["nmap", ip] instead of concatenated string."""

    # Prepare a fake request object with the minimal interface used by the view.
    class Req:
        method = "POST"

        class POSTDict(dict):
            def get(self, key, default=None):
                return super().get(key, default)

        POST = POSTDict({"ip": "127.0.0.1"})

    # Stub out command_out and regex parsing dependencies.
    mocker.patch.object(mitre, "command_out", return_value=(b"STATE SERVICE\n\n80/tcp open http\n", b""))

    # The view calls re.findall(pattern, res, re.DOTALL)[0] and then slices.
    # Provide output matching expected pattern to avoid unrelated failures.
    # Keep re.findall real.

    # Call the view; it returns a Django JsonResponse.
    resp = mitre.mitre_lab_17_api(Req())
    assert resp.status_code == 200

    data = resp.json()
    assert "ports" in data
    # Ensure command_out was called with argv list: ["nmap", "127.0.0.1"]
    mitre.command_out.assert_called_once()
    called_command = mitre.command_out.call_args[0][0]
    assert called_command == ["nmap", "127.0.0.1"]
