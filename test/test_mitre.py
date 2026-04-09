import introduction.mitre as mitre


def test_mitre_lab_17_api_uses_list_command_and_shell_false(monkeypatch):
    # Arrange: capture command passed to command_out
    captured = {}

    def fake_command_out(cmd):
        captured["cmd"] = cmd
        return (b"STATE SERVICE\n\n80/tcp open http\n\n", b"")

    monkeypatch.setattr(mitre, "command_out", fake_command_out)

    class _Req:
        method = "POST"

        class POST:
            @staticmethod
            def get(k):
                assert k == "ip"
                return "127.0.0.1"

    resp = mitre.mitre_lab_17_api(_Req())

    assert captured["cmd"] == ["nmap", "127.0.0.1"]
    assert resp.status_code == 200
