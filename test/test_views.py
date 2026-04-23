import pytest
from django.http import HttpRequest

from introduction import views


class _DummyUser:
    def __init__(self, authenticated: bool = True):
        self.is_authenticated = authenticated


class _PopenSpy:
    def __init__(self):
        self.called_with = None

    def __call__(self, *args, **kwargs):
        self.called_with = (args, kwargs)

        class _Proc:
            def communicate(self_inner):
                return (b"ok", b"")

        return _Proc()


def _make_post_request(domain: str, os_value: str) -> HttpRequest:
    req = HttpRequest()
    req.method = "POST"
    req.user = _DummyUser(True)
    req.POST = {"domain": domain, "os": os_value}
    return req


def test_cmd_lab_invokes_subprocess_without_shell_and_with_argv_list(monkeypatch):
    # Arrange
    popen_spy = _PopenSpy()
    monkeypatch.setattr(views.subprocess, "Popen", popen_spy)

    # An injection attempt: previously could have been interpreted by shell when shell=True
    request = _make_post_request("example.com; cat /etc/passwd", "win")

    # Act
    response = views.cmd_lab(request)

    # Assert: command should be passed as a list and shell should not be enabled
    args, kwargs = popen_spy.called_with
    assert isinstance(args[0], list)
    assert args[0][0] == "nslookup"
    assert "shell" not in kwargs or kwargs.get("shell") is False
    assert response.status_code == 200
