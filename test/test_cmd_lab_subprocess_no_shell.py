import pytest


def test_cmd_lab_uses_subprocess_without_shell(monkeypatch):
    """Regression test: cmd_lab must not use shell=True and must pass argv list."""
    # Import inside test so repo's module import errors surface naturally
    from introduction import views

    captured = {}

    class DummyPopen:
        def __init__(self, args, shell=False, stdout=None, stderr=None, **kwargs):
            captured['args'] = args
            captured['shell'] = shell
            self._stdout = b'out'
            self._stderr = b''

        def communicate(self):
            return self._stdout, self._stderr

    monkeypatch.setattr(views.subprocess, 'Popen', DummyPopen)

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        method = 'POST'
        user = DummyUser()
        POST = {'domain': 'example.com', 'os': 'linux'}

    # Act
    resp = views.cmd_lab(DummyRequest())

    # Assert
    assert captured['shell'] is False
    assert isinstance(captured['args'], list)
    assert captured['args'][0] in ('dig', 'nslookup')
    assert captured['args'][1] == 'example.com'
