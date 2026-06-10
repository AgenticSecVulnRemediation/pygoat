import subprocess

import pytest


@pytest.mark.parametrize(
    "domain",
    [
        "example.com;cat /etc/passwd",
        "example.com && whoami",
        "$(whoami)",
        "example.com|whoami",
        "example.com`whoami`",
        "example.com\nwhoami",
        "example.com/../../etc/passwd",
    ],
)
def test_cmd_lab_rejects_invalid_domain_characters(domain, client, django_user_model):
    # Arrange: authenticated user
    user = django_user_model.objects.create_user(username="u1", password="p1")
    client.force_login(user)

    # Act
    resp = client.post("/cmd/lab", {"domain": domain, "os": "linux"})

    # Assert: secure behavior is to reject invalid input
    assert resp.status_code == 400
    assert b"Invalid domain" in resp.content


def test_cmd_lab_executes_without_shell_and_uses_argument_list(mocker):
    """Regression test for command injection fix:

    Ensure subprocess.Popen is called with a list of args and shell is not enabled.
    """

    # Import lazily so patching works even if module import is heavy.
    from introduction import views

    # Arrange
    popen = mocker.patch.object(views.subprocess, "Popen")
    proc = mocker.Mock()
    proc.communicate.return_value = (b"ok", b"")
    popen.return_value = proc

    class _Req:
        method = "POST"
        user = mocker.Mock(is_authenticated=True)
        POST = {"domain": "example.com", "os": "linux"}

    req = _Req()

    # Act
    views.cmd_lab(req)

    # Assert
    args, kwargs = popen.call_args
    assert args[0] == ["dig", "example.com"]
    assert "shell" not in kwargs or kwargs.get("shell") is False
    assert kwargs.get("stdout") is subprocess.PIPE
    assert kwargs.get("stderr") is subprocess.PIPE
