import pytest
from django.http import HttpResponseBadRequest


@pytest.mark.django_db
def test_mitre_lab_17_api_rejects_invalid_ip(monkeypatch):
    """Regression: command injection fix validates IP and returns 400 for invalid input."""
    # Arrange
    from introduction import mitre

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        method = "POST"
        user = DummyUser()
        POST = {"ip": "1.2.3.4; touch /tmp/pwned"}

    # Ensure subprocess isn't invoked when input is invalid
    def fail_command_out(_cmd):
        raise AssertionError("command_out should not be called for invalid IP")

    monkeypatch.setattr(mitre, "command_out", fail_command_out)

    # Act
    response = mitre.mitre_lab_17_api(DummyRequest())

    # Assert
    assert isinstance(response, HttpResponseBadRequest)
    assert response.status_code == 400


@pytest.mark.django_db
def test_mitre_lab_17_api_uses_list_command_no_shell(monkeypatch):
    """Regression: command injection fix uses ['nmap', ip] and shell=False."""
    from introduction import mitre

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        method = "POST"
        user = DummyUser()
        POST = {"ip": "127.0.0.1"}

    captured = {}

    def fake_popen(cmd, shell, stdout, stderr):
        captured["cmd"] = cmd
        captured["shell"] = shell

        class Proc:
            def communicate(self):
                # Minimal output that matches the parsing regex
                out = b"STATE SERVICE\n\n22/tcp open ssh\n"
                err = b""
                return out, err

        return Proc()

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    # Act
    response = mitre.mitre_lab_17_api(DummyRequest())

    # Assert
    assert captured["cmd"] == ["nmap", "127.0.0.1"]
    assert captured["shell"] is False
    assert response.status_code == 200
