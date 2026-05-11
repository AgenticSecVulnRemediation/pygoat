# Assumption: 'introduction' is a Python package (has __init__.py) as typical for a Django app.

import subprocess


def test_mitre_lab_17_api_rejects_invalid_ip_and_does_not_invoke_subprocess(monkeypatch):
    """Delta: mitre_lab_17_api now validates IP and uses shell=False/list args.

    This test asserts that invalid IP is rejected and no subprocess is started.
    """
    from introduction import mitre

    popen_calls = []

    def _fake_popen(*args, **kwargs):
        popen_calls.append((args, kwargs))
        raise AssertionError("subprocess.Popen should not be invoked for invalid IP")

    monkeypatch.setattr(subprocess, "Popen", _fake_popen)

    class _Req:
        method = "POST"

        class POSTDict(dict):
            def get(self, k, default=None):
                return super().get(k, default)

        POST = POSTDict({"ip": "not_an_ip"})

    resp = mitre.mitre_lab_17_api(_Req())

    # Both PR variants return error, either HttpResponse(400) or JsonResponse
    assert getattr(resp, "status_code", None) in (200, 400)
    # Ensure subprocess isn't invoked on invalid input
    assert popen_calls == []


def test_command_out_uses_shell_false(monkeypatch):
    """Delta: command_out now sets shell=False."""
    from introduction import mitre

    observed = {}

    class _FakeProc:
        def communicate(self):
            return (b"", b"")

    def _fake_popen(cmd, **kwargs):
        observed["cmd"] = cmd
        observed["kwargs"] = kwargs
        return _FakeProc()

    monkeypatch.setattr(subprocess, "Popen", _fake_popen)

    mitre.command_out(["nmap", "127.0.0.1"])

    assert observed["kwargs"].get("shell") is False
