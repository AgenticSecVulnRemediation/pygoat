import json

import pytest

import introduction.mitre as mitre


class _FakeProcess:
    def __init__(self, stdout=b"", stderr=b""):
        self._stdout = stdout
        self._stderr = stderr

    def communicate(self):
        return self._stdout, self._stderr


def test_command_out_uses_shell_false(monkeypatch):
    """Regression: command_out must not invoke a shell (prevents command injection)."""
    captured = {}

    def fake_popen(command, shell, stdout, stderr):
        captured["command"] = command
        captured["shell"] = shell
        return _FakeProcess()

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    mitre.command_out(["nmap", "127.0.0.1"])

    assert captured["shell"] is False


@pytest.mark.parametrize(
    "ip",
    [
        "127.0.0.1; whoami",
        "1.2.3.4 && whoami",
        "not-an-ip",
        "127.0.0.1 | cat /etc/passwd",
    ],
)
def test_mitre_lab_17_api_rejects_invalid_ip(monkeypatch, ip):
    """Regression: invalid IP input must be rejected before building/executing command."""

    class _Req:
        method = "POST"

        class POST:
            @staticmethod
            def get(key):
                assert key == "ip"
                return ip

    # If validation is correct, we should never reach nmap invocation.
    def fail_if_called(*args, **kwargs):
        raise AssertionError("command_out must not be called for invalid IP")

    monkeypatch.setattr(mitre, "command_out", fail_if_called)

    resp = mitre.mitre_lab_17_api(_Req())

    # HttpResponseBadRequest is a subclass of HttpResponse with status_code set
    assert getattr(resp, "status_code", None) == 400


def test_mitre_lab_17_api_builds_list_command_for_valid_ip(monkeypatch):
    """Regression: command must be a list ['nmap', ip] (no string concatenation)."""

    class _Req:
        method = "POST"

        class POST:
            @staticmethod
            def get(key):
                assert key == "ip"
                return "127.0.0.1"

    # Provide an nmap-like output that matches the parser's regex.
    fake_output = (
        "STATE SERVICE\n\n"
        "80/tcp open http\n"
        "443/tcp open https\n"
        ""  # final newline not required by current logic
    ).encode("utf-8")

    captured = {}

    def fake_command_out(cmd):
        captured["cmd"] = cmd
        return fake_output, b""

    monkeypatch.setattr(mitre, "command_out", fake_command_out)

    # Avoid dependency on Django JsonResponse internals; just capture payload.
    class _FakeJsonResponse(dict):
        pass

    monkeypatch.setattr(mitre, "JsonResponse", lambda payload: _FakeJsonResponse(payload))

    resp = mitre.mitre_lab_17_api(_Req())

    assert captured["cmd"] == ["nmap", "127.0.0.1"]
    assert "ports" in resp
    assert "80/tcp open http" in resp["ports"]
