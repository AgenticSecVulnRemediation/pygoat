import types
import pytest

import introduction.mitre as mitre


def test_mitre_lab_17_api_rejects_invalid_ip(monkeypatch):
    class _Req:
        method = 'POST'
        POST = {'ip': '127.0.0.1; rm -rf /'}

    with pytest.raises(Exception, match='Invalid IP address provided'):
        mitre.mitre_lab_17_api(_Req())


def test_command_out_does_not_use_shell_true(monkeypatch):
    seen = {}

    class _P:
        def communicate(self):
            return (b"", b"")

    def _fake_popen(argv, stdout, stderr):
        # shell arg should not be present at all (defaults to False)
        seen['argv'] = argv
        return _P()

    monkeypatch.setattr(mitre.subprocess, 'Popen', _fake_popen)
    mitre.command_out(['nmap', '127.0.0.1'])
    assert seen['argv'] == ['nmap', '127.0.0.1']
