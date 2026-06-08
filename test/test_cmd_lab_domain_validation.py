import pytest


def test_cmd_lab_rejects_domain_with_shell_metacharacters(monkeypatch):
    """Regression test: domain validation must reject injection payloads."""
    from introduction import views

    # Prevent any accidental subprocess invocation
    def fail_popen(*args, **kwargs):
        raise AssertionError('subprocess.Popen should not be called for invalid domain')

    monkeypatch.setattr(views.subprocess, 'Popen', fail_popen)

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        method = 'POST'
        user = DummyUser()
        POST = {'domain': 'example.com; cat /etc/passwd', 'os': 'linux'}

    with pytest.raises(ValueError):
        views.cmd_lab(DummyRequest())
