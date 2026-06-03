import types

import pytest


def test_mitre_lab_17_api_requires_ip_and_rejects_invalid_ip(monkeypatch):
    import introduction.mitre as mitre

    # Arrange: make command_out fail if called; it must not be invoked for bad input
    monkeypatch.setattr(mitre, "command_out", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("command_out should not be called")))

    # Missing IP
    req_missing = types.SimpleNamespace(method="POST", POST={})
    resp = mitre.mitre_lab_17_api(req_missing)
    assert resp.status_code == 400

    # Invalid IP
    req_invalid = types.SimpleNamespace(method="POST", POST={"ip": "127.0.0.1; whoami"})
    resp2 = mitre.mitre_lab_17_api(req_invalid)
    assert resp2.status_code == 400


def test_command_out_uses_shell_false_and_list_command(monkeypatch):
    import introduction.mitre as mitre

    popen_args = {}

    class DummyProc:
        def communicate(self):
            return (b"ok", b"")

    def fake_popen(cmd, shell=False, stdout=None, stderr=None):
        popen_args["cmd"] = cmd
        popen_args["shell"] = shell
        return DummyProc()

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    out, err = mitre.command_out(["nmap", "8.8.8.8"])

    assert popen_args["cmd"] == ["nmap", "8.8.8.8"]
    assert popen_args["shell"] is False
    assert out == b"ok"
