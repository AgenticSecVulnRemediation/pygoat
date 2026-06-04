import pytest


def test_mitre_lab_17_api_rejects_non_ip_and_does_not_spawn_process(mocker):
    """Regression test for command injection: invalid IP returns 400 and does not execute nmap."""
    from introduction import mitre

    request = mocker.Mock()
    request.method = "POST"
    request.POST = {"ip": "127.0.0.1; rm -rf /"}

    popen_spy = mocker.patch.object(mitre.subprocess, "Popen", autospec=True)

    resp = mitre.mitre_lab_17_api(request)

    assert getattr(resp, "status_code", None) in (400,)
    popen_spy.assert_not_called()
