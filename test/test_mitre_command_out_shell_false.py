import pytest


def test_mitre_command_out_uses_shell_false(mocker):
    """Regression test for command injection: subprocess.Popen must be called with shell=False."""
    from introduction import mitre

    popen = mocker.patch.object(mitre.subprocess, "Popen", autospec=True)
    proc = mocker.Mock()
    proc.communicate.return_value = (b"out", b"")
    popen.return_value = proc

    out, err = mitre.command_out(["nmap", "127.0.0.1"])

    assert (out, err) == (b"out", b"")
    popen.assert_called_once()
    assert popen.call_args.kwargs.get("shell") is False
