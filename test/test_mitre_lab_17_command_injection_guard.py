import types
import pytest


def test_mitre_lab_17_api_rejects_non_ip_and_does_not_invoke_subprocess(monkeypatch):
    from introduction import mitre

    request = types.SimpleNamespace(method="POST", POST={"ip": "127.0.0.1; whoami"})

    def boom(_cmd):
        raise AssertionError("command_out should not be invoked for invalid IP")

    monkeypatch.setattr(mitre, "command_out", boom)

    with pytest.raises(ValueError):
        mitre.mitre_lab_17_api(request)


def test_command_out_uses_shell_false(monkeypatch):
    from introduction import mitre

    captured = {}

    class DummyProc:
        def __init__(self, *args, **kwargs):
            captured.update(kwargs)

        def communicate(self):
            return (b"", b"")

    monkeypatch.setattr(mitre.subprocess, "Popen", lambda *a, **kw: DummyProc(*a, **kw))

    mitre.command_out(["nmap", "127.0.0.1"])

    assert captured.get("shell") is False
