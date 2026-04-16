import subprocess
from types import SimpleNamespace

import pytest


@pytest.mark.parametrize(
    "bad_ip",
    [
        "1.2.3.4; rm -rf /",
        "127.0.0.1 && echo pwned",
        "not-an-ip",
        "256.1.1.1",
        "1.2.3",
        "",
    ],
)
def test_mitre_lab_17_api_rejects_invalid_ip_and_does_not_invoke_subprocess(monkeypatch, bad_ip):
    from introduction import mitre

    called = False

    def popen_fail(*args, **kwargs):
        nonlocal called
        called = True
        raise AssertionError("Popen should not be called for invalid ip")

    monkeypatch.setattr(subprocess, "Popen", popen_fail)

    request = SimpleNamespace(method="POST", POST={"ip": bad_ip})
    resp = mitre.mitre_lab_17_api(request)

    assert resp.status_code == 400
    assert called is False


def test_mitre_lab_17_api_uses_list_args_not_shell(monkeypatch):
    from introduction import mitre

    captured = {}

    class DummyPopen:
        def __init__(self, cmd, stdout=None, stderr=None, **kwargs):
            captured["cmd"] = cmd
            captured["kwargs"] = kwargs

        def communicate(self):
            return (b"STATE SERVICE\n\n22/tcp open ssh\n", b"")

    monkeypatch.setattr(subprocess, "Popen", DummyPopen)

    request = SimpleNamespace(method="POST", POST={"ip": "127.0.0.1"})
    resp = mitre.mitre_lab_17_api(request)

    assert resp.status_code == 200
    assert captured["cmd"] == ["nmap", "127.0.0.1"]
    assert captured["kwargs"].get("shell") is None
