# Assumptions:
# - Django project; we unit-test the view function directly with mocked request object.
# - We avoid importing full Django test client; only validate the changed validation behavior.

import types
import pytest


@pytest.mark.parametrize(
    "bad_domain",
    [
        "example.com; cat /etc/passwd",
        "example.com && whoami",
        "example.com | id",
        "http://example.com",
        "../evil.com",
        "",
    ],
)
def test_cmd_lab_rejects_invalid_domain_and_raises_value_error(monkeypatch, bad_domain):
    from introduction import views

    # Arrange: build a minimal request stub
    request = types.SimpleNamespace(
        user=types.SimpleNamespace(is_authenticated=True),
        method="POST",
        POST={"domain": bad_domain, "os": "win"},
    )

    # Prevent any subprocess usage if validation fails late
    def _boom(*args, **kwargs):
        raise AssertionError("subprocess should not be invoked for invalid domain")

    monkeypatch.setattr(views.subprocess, "Popen", _boom)

    # Act / Assert
    with pytest.raises(ValueError):
        views.cmd_lab(request)
