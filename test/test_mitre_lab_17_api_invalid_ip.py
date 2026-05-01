import pytest


# Assumptions:
# - pytest is used.


def _make_post_request(ip_value):
    class _Req:
        method = "POST"

        class _Post:
            @staticmethod
            def get(name):
                assert name == "ip"
                return ip_value

        POST = _Post()

    return _Req()


def test_mitre_lab_17_api_returns_400_for_invalid_ip_and_does_not_run_nmap(mocker):
    """Regression: invalid IP returns 400 JsonResponse and does not invoke subprocess."""
    from introduction import mitre

    popen = mocker.patch.object(mitre.subprocess, "Popen", autospec=True)

    req = _make_post_request("not-an-ip")

    resp = mitre.mitre_lab_17_api(req)

    popen.assert_not_called()
    # JsonResponse has status_code
    assert getattr(resp, "status_code", None) == 400
