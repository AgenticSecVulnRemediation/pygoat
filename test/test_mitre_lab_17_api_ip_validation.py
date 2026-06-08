import pytest


def test_mitre_lab_17_api_rejects_non_ip_input(monkeypatch):
    """Regression test: mitre_lab_17_api must return 400 for invalid IPs."""
    from introduction import mitre

    # Ensure no command execution can happen
    monkeypatch.setattr(mitre, 'command_out', lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError('command_out should not be called')))

    class DummyRequest:
        method = 'POST'
        POST = {'ip': '127.0.0.1; rm -rf /'}

    resp = mitre.mitre_lab_17_api(DummyRequest())
    assert getattr(resp, 'status_code', None) == 400
    assert b'Invalid IP address' in resp.content
