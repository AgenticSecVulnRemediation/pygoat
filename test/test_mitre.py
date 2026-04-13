import pytest


# Delta covered: command_out no longer uses shell=True and now receives argv list.

def test_command_out_uses_shell_false_and_list_command(mocker):
    from introduction import mitre

    popen_mock = mocker.patch.object(mitre.subprocess, "Popen")

    mitre.command_out(["nmap", "127.0.0.1"])

    assert popen_mock.call_count == 1
    args, kwargs = popen_mock.call_args
    assert args[0] == ["nmap", "127.0.0.1"]
    assert kwargs.get("shell") is False
