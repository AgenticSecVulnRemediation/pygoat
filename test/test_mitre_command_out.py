import importlib
import pytest


def test_command_out_does_not_use_shell_true(monkeypatch):
    mitre = importlib.import_module('introduction.mitre')

    captured = {}

    class DummyProc:
        def communicate(self):
            return (b'out', b'err')

    def fake_popen(command, stdout=None, stderr=None, **kwargs):
        captured['command'] = command
        captured['kwargs'] = kwargs
        return DummyProc()

    monkeypatch.setattr(mitre.subprocess, 'Popen', fake_popen)

    # Act
    out, err = mitre.command_out(['echo', 'hi'])

    # Assert
    assert out == b'out'
    assert err == b'err'
    assert captured['command'] == ['echo', 'hi']
    # Regression: shell should not be enabled
    assert 'shell' not in captured['kwargs']


def test_mitre_lab_17_api_builds_argument_list_for_nmap(monkeypatch):
    mitre = importlib.import_module('introduction.mitre')

    # Patch command_out to avoid running nmap and to validate args
    def fake_command_out(cmd):
        assert cmd == ['nmap', '127.0.0.1']
        # Minimal output that matches the regex in the function
        res = b"STATE SERVICE\n\n22/tcp open ssh\n"
        return res, b''

    monkeypatch.setattr(mitre, 'command_out', fake_command_out)

    # Patch JsonResponse to avoid Django dependency; return python dict instead
    monkeypatch.setattr(mitre, 'JsonResponse', lambda d: d)

    class DummyRequest:
        method = 'POST'

        def __init__(self):
            self.POST = {'ip': '127.0.0.1'}

    resp = mitre.mitre_lab_17_api(DummyRequest())
    assert resp['ports'] == ['22/tcp open ssh']
