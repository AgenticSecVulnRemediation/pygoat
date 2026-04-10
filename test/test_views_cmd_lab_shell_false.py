import subprocess

import pytest


def test_cmd_lab_uses_shell_false_and_argv_list(monkeypatch):
    # Regression test: ensure subprocess.Popen is invoked with shell=False and argv list.
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

    class Req:
        user = type('U', (), {'is_authenticated': True})()
        method = 'POST'
        POST = {'domain': 'example.com', 'os': 'win'}

    views.cmd_lab(Req())

    assert captured['cmd'] == ["nslookup", "example.com"]
    assert captured['kwargs'].get('shell') is False
