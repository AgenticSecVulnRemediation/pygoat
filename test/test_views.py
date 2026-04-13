import pytest


# Delta covered: cmd_lab no longer uses shell=True and now uses argv list for subprocess.Popen.

def test_cmd_lab_uses_argv_list_and_shell_false(mocker):
    from introduction import views

    popen_mock = mocker.patch.object(views.subprocess, "Popen")
    render_mock = mocker.patch.object(views, "render", return_value="OK")

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        method = "POST"
        user = DummyUser()

        def __init__(self, domain: str, os_value: str):
            self.POST = {"domain": domain, "os": os_value}

    req = DummyRequest(domain="example.com;rm -rf /", os_value="win")

    # Act
    views.cmd_lab(req)

    # Assert: command must be list and shell must not be used
    assert popen_mock.call_count == 1
    args, kwargs = popen_mock.call_args
    assert isinstance(args[0], list)
    assert kwargs.get("shell", False) is False
    render_mock.assert_called()
