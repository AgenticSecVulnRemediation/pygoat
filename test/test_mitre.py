import pytest


# Assumptions:
# - Django app module path is `introduction.mitre`.
# - We unit-test only the new IP validation and non-shell subprocess invocation.


def _make_request(ip_value, method="POST"):
    class _Request:
        method = method
        POST = {"ip": ip_value}

    return _Request()


def test_mitre_lab_17_api_rejects_invalid_ip(monkeypatch):
    from introduction import mitre

    request = _make_request("127.0.0.1; rm -rf /")

    resp = mitre.mitre_lab_17_api(request)

    assert resp.status_code == 400


def test_mitre_lab_17_api_uses_list_command_no_shell(monkeypatch):
    from introduction import mitre

    request = _make_request("127.0.0.1")

    popen_calls = {}

    class FakeProc:
        def communicate(self):
            # Minimal nmap-like output matching the regex used in the view.
            out = b"STATE SERVICE\n\n80/tcp open http\n"
            err = b""
            return out, err

    def fake_popen(cmd, stdout=None, stderr=None, **kwargs):
        popen_calls["cmd"] = cmd
        popen_calls["kwargs"] = kwargs
        return FakeProc()

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    resp = mitre.mitre_lab_17_api(request)

    assert resp.status_code == 200
    assert popen_calls["cmd"] == ["nmap", "127.0.0.1"]
    assert "shell" not in popen_calls["kwargs"]
