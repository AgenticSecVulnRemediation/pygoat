# Assumption: Django app module is named `introduction` (based on file path).

import types

import pytest


@pytest.mark.parametrize(
    "bad_ip",
    [
        "127.0.0.1; whoami",
        "127.0.0.1 && whoami",
        "127.0.0.1 | whoami",
        "$(whoami)",
        "not-an-ip",
        "",
        None,
    ],
)
def test_mitre_lab_17_api_rejects_invalid_ip_and_does_not_execute_subprocess(monkeypatch, bad_ip):
    """Delta test for command-injection fix.

    Changed behavior:
    - validate IP input
    - build subprocess command as argv list (no shell)
    - reject invalid input before executing nmap
    """

    # Import here so the monkeypatch applies even if module-level imports occur elsewhere.
    import introduction.mitre as mitre

    # Arrange: fail the test if subprocess.Popen is ever called
    def _popen_should_not_be_called(*args, **kwargs):
        raise AssertionError("subprocess.Popen should not be called for invalid IP input")

    monkeypatch.setattr(mitre.subprocess, "Popen", _popen_should_not_be_called)

    class DummyRequest:
        method = "POST"

        class _POST:
            def __init__(self, v):
                self._v = v

            def get(self, key):
                assert key == "ip"
                return self._v

        POST = _POST(bad_ip)

    # Act
    resp = mitre.mitre_lab_17_api(DummyRequest())

    # Assert: both variants return an HttpResponse with these semantics
    # - PR 1932 returns HttpResponse("Invalid IP address")
    # - PR 1931 returns HttpResponseBadRequest("Invalid IP address")
    assert getattr(resp, "content", b"").decode("utf-8") == "Invalid IP address"
