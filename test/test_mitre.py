import json
import subprocess
from unittest.mock import Mock

import pytest


# Assumption: module path is introduction.mitre as indicated by file_path.
from introduction.mitre import command_out, mitre_lab_17_api


def test_command_out_uses_shell_false(monkeypatch):
    """Regression: command_out must invoke subprocess without shell=True."""

    def fake_popen(*args, **kwargs):
        # Assert changed behavior: shell must be False (mitigates command injection)
        assert kwargs.get("shell") is False
        proc = Mock()
        proc.communicate.return_value = (b"ok", b"")
        return proc

    monkeypatch.setattr(subprocess, "Popen", fake_popen)

    out, err = command_out(["echo", "hello"])
    assert out == b"ok"
    assert err == b""


def test_mitre_lab_17_api_rejects_invalid_ip(mocker):
    """Security: invalid IPs must be rejected before reaching subprocess."""
    request = Mock()
    request.method = "POST"
    request.POST = {"ip": "127.0.0.1; whoami"}

    popen_spy = mocker.patch("subprocess.Popen")

    resp = mitre_lab_17_api(request)

    assert resp.status_code == 400
    popen_spy.assert_not_called()
