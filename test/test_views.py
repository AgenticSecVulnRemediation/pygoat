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


def test_cmd_lab_uses_list_command_and_no_shell(monkeypatch):
    # Arrange
    seen = {}

    def fake_popen(cmd, stdout, stderr):
        seen["cmd"] = cmd

        class P:
            def communicate(self):
                return (b"ok", b"")

        return P()

    monkeypatch.setattr(views.subprocess, "Popen", fake_popen)

    # Act
    resp = views.cmd_lab(_make_request("example.com", os_value="win"))

    # Assert
    assert seen["cmd"] == ["nslookup", "example.com"]
    assert resp.status_code == 200


def test_cmd_lab_does_not_allow_command_injection_payload(monkeypatch):
    # Arrange
    def fail_popen(*args, **kwargs):
        raise AssertionError("Popen must not be called when domain is invalid")

    monkeypatch.setattr(views.subprocess, "Popen", fail_popen)

    # Act
    resp = views.cmd_lab(_make_request("example.com; whoami", os_value="win"))

    # Assert
    # Handler catches exception and shows generic error
    assert "Something went wrong" in str(resp.content)
