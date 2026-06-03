import types


def test_mitre_lab_17_api_validates_ip_and_does_not_execute_shell(monkeypatch):
    import introduction.mitre as mitre

    captured = {}

    def fake_command_out(cmd):
        captured["cmd"] = cmd
        return (b"STATE SERVICE\n\n80/tcp open http\n", b"")

    monkeypatch.setattr(mitre, "command_out", fake_command_out)

    # Act
    req = types.SimpleNamespace(method="POST", POST={"ip": "8.8.8.8"})
    resp = mitre.mitre_lab_17_api(req)

    # Assert: command is passed as list (shell injection resistant)
    assert captured["cmd"] == ["nmap", "8.8.8.8"]
    assert resp.status_code == 200
