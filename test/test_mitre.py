import pytest


# Assumptions:
# - Django view is available at introduction.mitre.mitre_lab_17_api
# - We test input validation and subprocess invocation shape.


def _make_request(ip):
    class _Req:
        method = "POST"
        POST = {"ip": ip}
    return _Req()


def test_mitre_lab_17_api_rejects_invalid_ip(monkeypatch):
    from introduction import mitre

    # If IP is invalid, we should not execute nmap at all.
    called = {"popen": False}

    def fake_popen(*args, **kwargs):
        called["popen"] = True
        raise AssertionError("subprocess.Popen should not be called for invalid IP")

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    resp = mitre.mitre_lab_17_api(_make_request("127.0.0.1; rm -rf /"))

    assert resp.status_code == 400
    assert called["popen"] is False


def test_mitre_lab_17_api_executes_nmap_without_shell(monkeypatch):
    from introduction import mitre

    popen_args = {}

    class FakeProc:
        def communicate(self):
            # minimal output matching parser expectations
            out = b"STATE SERVICE\n\n80/tcp open http\n\n"
            err = b""
            return out, err

    def fake_popen(cmd, stdout=None, stderr=None, shell=None, **kwargs):
        popen_args["cmd"] = cmd
        popen_args["shell"] = shell
        return FakeProc()

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    resp = mitre.mitre_lab_17_api(_make_request("127.0.0.1"))

    assert resp.status_code == 200
    assert popen_args["cmd"] == ["nmap", "127.0.0.1"]
    # In fixed code, shell argument should not be enabled (None/False)
    assert popen_args["shell"] in (None, False)
