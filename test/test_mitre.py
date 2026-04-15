import pytest


def _import_mitre_safely():
    try:
        import introduction.mitre as mitre
        return mitre
    except Exception:
        pytest.skip("Django environment not available; skipping unit-level import test")


def test_mitre_lab_17_api_rejects_invalid_ip(monkeypatch):
    mitre = _import_mitre_safely()

    class DummyRequest:
        method = "POST"

        def __init__(self, ip):
            self.POST = {"ip": ip}

    # If invalid IP is supplied, code should return HttpResponseBadRequest before calling command_out.
    monkeypatch.setattr(
        mitre,
        "command_out",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("command_out should not be called")),
    )

    resp = mitre.mitre_lab_17_api(DummyRequest("127.0.0.1; rm -rf /"))
    assert getattr(resp, "status_code", None) == 400


def test_command_out_does_not_use_shell_true(monkeypatch):
    mitre = _import_mitre_safely()

    popen_calls = {}

    class DummyPopen:
        def __init__(self, command, shell, stdout, stderr):
            popen_calls["shell"] = shell
            popen_calls["command"] = command

        def communicate(self):
            return (b"", b"")

    monkeypatch.setattr(mitre.subprocess, "Popen", DummyPopen)

    mitre.command_out(["nmap", "127.0.0.1"])

    assert popen_calls["shell"] is False
    assert popen_calls["command"] == ["nmap", "127.0.0.1"]
