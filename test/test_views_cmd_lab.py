import re
import importlib
import pytest


def test_cmd_lab_rejects_invalid_domain_characters_before_exec(monkeypatch):
    views = importlib.import_module('introduction.views')

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        user = DummyUser()
        method = 'POST'

        def __init__(self):
            self.POST = {'domain': 'example.com; rm -rf /', 'os': 'linux'}

    # Ensure subprocess is never invoked when input is invalid
    def popen_fail(*args, **kwargs):
        raise AssertionError('subprocess.Popen should not be called for invalid domain')

    monkeypatch.setattr(views.subprocess, 'Popen', popen_fail)

    with pytest.raises(ValueError, match=re.escape('Invalid domain')):
        views.cmd_lab(DummyRequest())
