# Assumptions:
# - Django project uses standard layout where the "introduction" app is importable.
# - Tests are executed with pytest-django configured (DJANGO_SETTINGS_MODULE set).

import subprocess

import pytest


@pytest.fixture(autouse=True)
def _no_real_subprocess(monkeypatch):
    """Prevent any accidental real subprocess execution in tests."""

    def _blocked(*args, **kwargs):
        raise AssertionError("subprocess should not be executed during unit tests")

    monkeypatch.setattr(subprocess, "Popen", _blocked)


def test_mitre_lab_17_api_rejects_invalid_ip_and_does_not_invoke_subprocess(monkeypatch):
    """Regression: input IP is validated; invalid values return 400 before building a command."""
    from introduction import mitre

    # Arrange: make sure even if code path tries to execute, we can detect it
    called = {"count": 0}

    def _command_out(_cmd):
        called["count"] += 1
        return (b"", b"")

    monkeypatch.setattr(mitre, "command_out", _command_out)

    class Req:
        method = "POST"

        class POST:
            @staticmethod
            def get(_k):
                return "1.2.3.4; rm -rf /"  # not an IP

    # Act
    resp = mitre.mitre_lab_17_api(Req())

    # Assert
    assert resp.status_code == 400
    assert called["count"] == 0


def test_mitre_lab_17_api_valid_ip_calls_command_out_with_argv_and_shell_is_false(monkeypatch):
    """Regression: command execution uses argv list and shell=False."""
    from introduction import mitre

    # Arrange: capture the exact command passed to command_out
    captured = {}

    def _command_out(cmd):
        captured["cmd"] = cmd
        return (b"STATE SERVICE\n\n22/tcp open ssh\n", b"")

    monkeypatch.setattr(mitre, "command_out", _command_out)

    class Req:
        method = "POST"

        class POST:
            @staticmethod
            def get(_k):
                return "127.0.0.1"

    # Act
    resp = mitre.mitre_lab_17_api(Req())

    # Assert
    assert resp.status_code == 200
    assert captured["cmd"] == ["nmap", "127.0.0.1"]
