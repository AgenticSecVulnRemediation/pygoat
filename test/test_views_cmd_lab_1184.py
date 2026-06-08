import types
import pytest

import introduction.views as views


class _DummyPopen:
    def __init__(self, argv, shell, stdout, stderr):
        self.argv = argv
        self.shell = shell
        self._stdout = stdout
        self._stderr = stderr

    def communicate(self):
        return (b"OK", b"")


def test_cmd_lab_uses_shell_false_and_argv_list(monkeypatch):
    """Regression for command injection fix: Popen must be invoked with shell=False and argv list."""

    popen_calls = {}

    def _fake_popen(argv, shell, stdout, stderr):
        popen_calls['argv'] = argv
        popen_calls['shell'] = shell
        return _DummyPopen(argv, shell, stdout, stderr)

    monkeypatch.setattr(views.subprocess, 'Popen', _fake_popen)

    class _Req:
        method = 'POST'
        user = types.SimpleNamespace(is_authenticated=True)
        POST = {'domain': 'example.com;whoami', 'os': 'linux'}

    # Stub render to avoid templates
    monkeypatch.setattr(views, 'render', lambda request, template, context=None: {'template': template, 'context': context})

    resp = views.cmd_lab(_Req())

    assert popen_calls['shell'] is False
    assert popen_calls['argv'][0] == 'dig'
    assert popen_calls['argv'][1].startswith('example.com')
    assert ';' in _Req.POST['domain']  # input still contains metachar but should not be shell-interpreted
    assert resp['template'].endswith('cmd_lab.html')
