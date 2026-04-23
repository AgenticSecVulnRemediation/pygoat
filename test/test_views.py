import pytest
from django.http import HttpRequest

from introduction import views


class _DummyUser:
    def __init__(self, authenticated: bool = True):
        self.is_authenticated = authenticated


def _make_post_request(domain: str, os_value: str) -> HttpRequest:
    req = HttpRequest()
    req.method = "POST"
    req.user = _DummyUser(True)
    req.POST = {"domain": domain, "os": os_value}
    return req


def test_cmd_lab_rejects_domain_with_shell_metacharacters_returns_400():
    # Arrange: attempt shell injection that should now be rejected by strict regex
    request = _make_post_request("example.com;cat/etc/passwd", "win")

    # Act
    response = views.cmd_lab(request)

    # Assert
    assert response.status_code == 400
    assert b"Invalid domain" in response.content
