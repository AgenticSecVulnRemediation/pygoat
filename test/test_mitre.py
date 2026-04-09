import introduction.mitre as mitre


def test_command_out_uses_shell_false(monkeypatch):
    # Assert the fix: subprocess.Popen is invoked with shell=False
    called = {}

    class FakeProc:
        def communicate(self):
            return (b"", b"")

    def fake_popen(command, shell, stdout, stderr):
        called["shell"] = shell
        called["command"] = command
        return FakeProc()

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    mitre.command_out(["nmap", "127.0.0.1"])

    assert called["shell"] is False


def test_mitre_lab_17_api_rejects_invalid_ip(monkeypatch):
    # Arrange: invalid IP should short-circuit before calling command_out
    monkeypatch.setattr(mitre, "command_out", lambda cmd: (_ for _ in ()).throw(AssertionError("command_out should not be called")))

    class _Req:
        method = "POST"

        class POST:
            @staticmethod
            def get(k):
                assert k == "ip"
                return "127.0.0.1; rm -rf /"

    resp = mitre.mitre_lab_17_api(_Req())

    assert resp.status_code == 400
