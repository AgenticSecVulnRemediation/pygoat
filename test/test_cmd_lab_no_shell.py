import subprocess

import pytest


class _FakeReq:
    def __init__(self, os_name: str, domain: str):
        self.user = type("U", (), {"is_authenticated": True})()
        self.method = "POST"
        self.POST = {"os": os_name, "domain": domain}


@pytest.mark.parametrize(
    "os_name,expected_executable",
    [
        ("win", "nslookup"),
        ("linux", "dig"),
    ],
)
def test_cmd_lab_invokes_subprocess_with_argv_list_and_no_shell(mocker, os_name, expected_executable):
    """Regression test for command injection hardening in cmd_lab.

    Patch changed command from formatted string + shell=True to argv list and no shell.
    """

    from introduction import views

    popen_mock = mocker.patch.object(subprocess, "Popen", autospec=True)
    popen_mock.return_value.communicate.return_value = (b"ok", b"")

    # Make render return a simple object; we only care that we reach Popen.
    mocker.patch.object(views, "render", autospec=True, return_value=object())

    req = _FakeReq(os_name=os_name, domain="example.com;rm -rf /")
    views.cmd_lab(req)

    assert popen_mock.call_count == 1
    argv = popen_mock.call_args.args[0]
    assert isinstance(argv, list)
    assert argv[0] == expected_executable

    assert popen_mock.call_args.kwargs.get("shell") is None
