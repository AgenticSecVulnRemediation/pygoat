import pytest


def _make_request(ip: str):
    class _Req:
        method = "POST"
        POST = {"ip": ip}

    return _Req()


def test_mitre_lab_17_api_rejects_invalid_ip_and_does_not_execute_subprocess(monkeypatch):
    from introduction import mitre

    def fake_popen(*args, **kwargs):
        raise AssertionError("subprocess.Popen must not be called for invalid IP")

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    resp = mitre.mitre_lab_17_api(_make_request("127.0.0.1; rm -rf /"))

    assert resp.status_code == 400


def test_mitre_lab_17_api_uses_argv_and_shell_is_not_enabled(monkeypatch):
    from introduction import mitre

    captured = {}

    class FakeProc:
        def communicate(self):
            # minimal output matching parser expectations
            return (b"STATE SERVICE\n\n80/tcp open http\n\n", b"")

    def fake_popen(cmd, stdout=None, stderr=None, shell=None, **kwargs):
        captured["cmd"] = cmd
        captured["shell"] = shell
        return FakeProc()

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    resp = mitre.mitre_lab_17_api(_make_request("127.0.0.1"))

    assert resp.status_code == 200
    assert captured["cmd"] == ["nmap", "127.0.0.1"]
    assert captured["shell"] in (None, False)
