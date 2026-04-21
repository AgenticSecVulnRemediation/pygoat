import types

import pytest

# Assumption: module path is importable as introduction.views
from introduction import views


def _make_request(domain, os_value="win"):
    user = types.SimpleNamespace(is_authenticated=True)
    req = types.SimpleNamespace()
    req.method = "POST"
    req.POST = {"domain": domain, "os": os_value}
    req.user = user
    return req


def test_cmd_lab_rejects_invalid_domain_before_subprocess(monkeypatch):
    # Arrange
    def fail_popen(*args, **kwargs):
        raise AssertionError("Popen must not be called for invalid domain")

    monkeypatch.setattr(views.subprocess, "Popen", fail_popen)

    # Act
    resp = views.cmd_lab(_make_request("example.com;whoami", os_value="win"))

    # Assert
    assert "Something went wrong" in str(resp.content)


def test_cmd_lab_uses_shell_false_and_list_command(monkeypatch):
    # Arrange
    seen = {}

    def fake_popen(cmd, shell, stdout, stderr):
        seen["cmd"] = cmd
        seen["shell"] = shell

        class P:
            def communicate(self):
                return (b"ok", b"")

        return P()

    monkeypatch.setattr(views.subprocess, "Popen", fake_popen)

    # Act
    resp = views.cmd_lab(_make_request("example.com", os_value="linux"))

    # Assert
    assert seen["cmd"] == ["dig", "example.com"]
    assert seen["shell"] is False
    assert resp.status_code == 200
