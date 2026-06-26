import pytest


from introduction import views


@pytest.mark.parametrize(
    "domain",
    [
        "example.com; rm -rf /",
        "example.com && whoami",
        "example.com | cat /etc/passwd",
        "example.com$(touch /tmp/pwn)",
        "example.com`id`",
    ],
)
def test_cmd_lab_rejects_malicious_domain_input(domain, mocker):
    """Regression for command injection: invalid domain must be rejected with 400."""
    # Arrange
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"
    request.POST.get.side_effect = lambda k: {"domain": domain, "os": "nix"}[k]

    http_response_mock = mocker.patch("introduction.views.HttpResponse")
    popen_mock = mocker.patch("introduction.views.subprocess.Popen")

    # Act
    views.cmd_lab(request)

    # Assert
    http_response_mock.assert_called_once()
    _, kwargs = http_response_mock.call_args
    assert kwargs.get("status") == 400
    assert popen_mock.call_count == 0


def test_cmd_lab_executes_with_shell_false_and_list_args(mocker):
    """When domain is valid, subprocess should be called with argv list and shell disabled."""
    # Arrange
    request = mocker.Mock()
    request.user.is_authenticated = True
    request.method = "POST"
    request.POST.get.side_effect = lambda k: {"domain": "example.com", "os": "win"}[k]

    proc = mocker.Mock()
    proc.communicate.return_value = (b"ok", b"")
    popen_mock = mocker.patch("introduction.views.subprocess.Popen", return_value=proc)
    render_mock = mocker.patch("introduction.views.render", return_value=mocker.Mock())

    # Act
    views.cmd_lab(request)

    # Assert
    args, kwargs = popen_mock.call_args
    assert args[0] == ["nslookup", "example.com"]
    assert "shell" not in kwargs or kwargs.get("shell") is False
    render_mock.assert_called()
