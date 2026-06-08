# Assumption: Django app module is importable as `introduction.views` in test environment.
# This test targets the command injection hardening in cmd_lab: validate domain and avoid shell=True.

import pytest


def _build_request(domain: str, os_value: str = "nix", authenticated: bool = True):
    class _User:
        def __init__(self, authed: bool):
            self.is_authenticated = authed

    class _Req:
        def __init__(self, dom: str, os_val: str, authed: bool):
            self.user = _User(authed)
            self.method = "POST"
            self.POST = {"domain": dom, "os": os_val}

    return _Req(domain, os_value, authenticated)


def test_cmd_lab_with_invalid_domain_characters_raises_value_error(mocker):
    """After the patch, domains not matching ^[a-zA-Z0-9.-]+$ are rejected.

    This prevents payloads like `example.com; cat /etc/passwd` from reaching subprocess.
    """
    import introduction.views as views

    req = _build_request("example.com;cat /etc/passwd")

    # Mock render to ensure we don't need templates; should not be called on ValueError
    render_mock = mocker.patch.object(views, "render")

    with pytest.raises(ValueError, match="Invalid domain value provided"):
        views.cmd_lab(req)

    render_mock.assert_not_called()


def test_cmd_lab_uses_argv_list_and_does_not_enable_shell(mocker):
    """After the patch, Popen should be called with a list argv and without shell=True."""
    import introduction.views as views

    req = _build_request("example.com", os_value="win")

    popen_mock = mocker.patch.object(views.subprocess, "Popen")
    proc = mocker.Mock()
    proc.communicate.return_value = (b"ok", b"")
    popen_mock.return_value = proc

    # Mock render to avoid templates
    mocker.patch.object(views, "render", return_value={"ok": True})

    views.cmd_lab(req)

    # Assert argv list
    args, kwargs = popen_mock.call_args
    assert args[0] == ["nslookup", "example.com"]
    # Assert no shell kwarg (or explicitly False)
    assert "shell" not in kwargs or kwargs["shell"] is False
