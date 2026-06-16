import subprocess
import pytest
from django.test import RequestFactory

from introduction.mitre import mitre_lab_17_api


@pytest.mark.django_db
def test_mitre_lab_17_api_builds_list_command_and_shell_false(monkeypatch):
    # This PR change replaces shell=True/string command with shell=False/list args.
    rf = RequestFactory()
    request = rf.post('/mitre/17/lab/api', data={'ip': '127.0.0.1'})

    captured = {}

    class DummyProc:
        def __init__(self, args, **kwargs):
            captured['args'] = args
            captured['kwargs'] = kwargs

        def communicate(self):
            out = b"STATE SERVICE\n\n22/tcp open ssh\n"
            err = b""
            return out, err

    monkeypatch.setattr(subprocess, 'Popen', lambda *a, **kw: DummyProc(*a, **kw))

    response = mitre_lab_17_api(request)

    assert response.status_code == 200
    assert captured['args'] == ['nmap', '127.0.0.1']
    assert captured['kwargs'].get('shell', False) is False
