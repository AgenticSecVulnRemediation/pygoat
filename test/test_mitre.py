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
    # Import module under test
    from introduction import mitre

    popen_called = False

    def popen_fail(*args, **kwargs):
        nonlocal popen_called
        popen_called = True
        raise AssertionError("subprocess.Popen should not be called for invalid IP")

    monkeypatch.setattr(subprocess, "Popen", popen_fail)

    # Build minimal request-like object
    request = SimpleNamespace(method="POST", POST={"ip": bad_ip})

    resp = mitre.mitre_lab_17_api(request)

    assert resp.status_code == 400
    assert popen_called is False


def test_mitre_lab_17_api_uses_argument_list_for_subprocess(monkeypatch):
    from introduction import mitre

    captured = {}

    class DummyPopen:
        def __init__(self, cmd, stdout=None, stderr=None, **kwargs):
            captured["cmd"] = cmd
            captured["kwargs"] = kwargs

        def communicate(self):
            # Provide output matching regex used in handler
            out = b"STATE SERVICE\n\n22/tcp open ssh\n"
            err = b""
            return out, err

    monkeypatch.setattr(subprocess, "Popen", DummyPopen)

    request = SimpleNamespace(method="POST", POST={"ip": "127.0.0.1"})
    resp = mitre.mitre_lab_17_api(request)

    assert resp.status_code == 200
    assert captured["cmd"] == ["nmap", "127.0.0.1"]
    # Ensure 'shell' is not passed/enabled implicitly
    assert captured["kwargs"].get("shell") is None
