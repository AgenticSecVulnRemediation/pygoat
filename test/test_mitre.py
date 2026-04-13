import json
from types import SimpleNamespace

import pytest

# Assumption: Django app module path is introduction.mitre
from introduction import mitre


def _make_request(ip_value: str):
    return SimpleNamespace(method="POST", POST={"ip": ip_value})


def test_mitre_lab_17_api_rejects_invalid_ip_and_does_not_invoke_subprocess(monkeypatch):
    # Arrange
    request = _make_request("127.0.0.1; touch /tmp/pwned")

    popen_called = {"called": False}

    def fake_popen(*args, **kwargs):
        popen_called["called"] = True
        raise AssertionError("subprocess.Popen should not be called for invalid IP")

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    # Act
    response = mitre.mitre_lab_17_api(request)

    # Assert
    assert response.status_code == 400
    payload = json.loads(response.content.decode("utf-8"))
    assert payload["error"] == "Invalid IP address"
    assert popen_called["called"] is False


def test_mitre_lab_17_api_uses_argv_list_for_nmap(monkeypatch):
    # Arrange
    request = _make_request("127.0.0.1")

    captured = {"args": None, "kwargs": None}

    class FakeProcess:
        def communicate(self):
            # Minimal output to satisfy the regex parsing in mitre_lab_17_api
            out = b"STATE SERVICE\n\n22/tcp open ssh\n"
            err = b""
            return out, err

    def fake_popen(*args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs
        return FakeProcess()

    monkeypatch.setattr(mitre.subprocess, "Popen", fake_popen)

    # Act
    response = mitre.mitre_lab_17_api(request)

    # Assert
    assert response.status_code == 200
    assert captured["args"][0] == ["nmap", "127.0.0.1"]
    assert captured["kwargs"].get("shell") is None
