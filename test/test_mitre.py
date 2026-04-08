import types
import pytest


# Assumption: Django app module path is introduction.mitre
# Tests focus only on the command injection mitigation: validate IP and avoid shell=True.


def _make_request(ip_value, method="POST"):
    return types.SimpleNamespace(method=method, POST={"ip": ip_value})


def test_mitre_lab_17_api_rejects_invalid_ip(monkeypatch):
    import introduction.mitre as mitre

    request = _make_request("127.0.0.1; rm -rf /")

    # Ensure command_out is not called for invalid IP
    monkeypatch.setattr(mitre, 'command_out', lambda *_a, **_k: (_ for _ in ()).throw(AssertionError('command_out should not be called')))

    resp = mitre.mitre_lab_17_api(request)

    # HttpResponseBadRequest has status_code 400
    assert getattr(resp, 'status_code', None) == 400


def test_mitre_lab_17_api_uses_list_command(monkeypatch):
    import introduction.mitre as mitre

    request = _make_request("127.0.0.1")

    captured = {"cmd": None}

    def fake_command_out(cmd):
        captured["cmd"] = cmd
        # Return output that matches the regex used by the view
        res = b"STATE SERVICE\n\n80/tcp open http\n"
        err = b""
        return res, err

    monkeypatch.setattr(mitre, 'command_out', fake_command_out)

    resp = mitre.mitre_lab_17_api(request)

    assert captured["cmd"] == ["nmap", "127.0.0.1"]
    # JsonResponse has status_code 200
    assert getattr(resp, 'status_code', None) == 200
