import subprocess

import pytest


def test_cmd_lab_uses_subprocess_without_shell_true(monkeypatch):
    # Regression test: ensure subprocess.Popen is invoked without shell=True and with argv list.
    from introduction import views

    captured = {}

    class DummyProc:
        def communicate(self):
            return (b'out', b'')

    def fake_popen(cmd, *args, **kwargs):
        captured['cmd'] = cmd
        captured['kwargs'] = kwargs
        return DummyProc()

    monkeypatch.setattr(subprocess, 'Popen', fake_popen)

    # Call the view function directly with a minimal request stub.
    class Req:
        user = type('U', (), {'is_authenticated': True})()
        method = 'POST'
        POST = {'domain': 'example.com', 'os': 'win'}

    # The view returns a Django HttpResponse; we only care that Popen was called securely.
    views.cmd_lab(Req())

    assert captured['cmd'] == ['nslookup', 'example.com']
    assert captured['kwargs'].get('shell', False) is False
