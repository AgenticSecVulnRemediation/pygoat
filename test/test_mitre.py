import types

import introduction.mitre as mitre


class _FakeRequest:
    def __init__(self, ip: str):
        self.method = "POST"
        self.POST = {"ip": ip}


def test_mitre_lab_17_api_rejects_invalid_ip_returns_400(monkeypatch):
    """Regression: IP is validated; injection payloads must be rejected with HTTP 400."""
    # Arrange: decorator should not block unit test
    monkeypatch.setattr(mitre, "authentication_decorator", lambda f: f)

    # Ensure no subprocess execution happens
    monkeypatch.setattr(mitre, "command_out", lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("command_out should not be called")))

    # Act
    resp = mitre.mitre_lab_17_api(_FakeRequest("127.0.0.1; rm -rf /"))

    # Assert
    assert getattr(resp, "status_code", None) == 400


def test_command_out_splits_string_command_and_does_not_use_shell(monkeypatch):
    """Regression: command_out must not invoke a shell and must accept string input safely."""

    captured = {}

    class _Proc:
        def communicate(self):
            return (b"ok", b"")

    def _fake_popen(cmd, stdout=None, stderr=None, **kwargs):
        captured["cmd"] = cmd
        captured["kwargs"] = kwargs
        return _Proc()

    monkeypatch.setattr(mitre.subprocess, "Popen", _fake_popen)

    out, err = mitre.command_out("nmap 127.0.0.1")

    assert out == b"ok"
    assert err == b""
    assert captured["cmd"] == ["nmap", "127.0.0.1"]
    assert "shell" not in captured["kwargs"]
