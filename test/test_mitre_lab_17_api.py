import pytest


# Assumptions:
# - pytest is used.
# - We can import introduction.mitre directly.


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


def test_mitre_lab_17_api_rejects_invalid_ip_before_running_subprocess(mocker):
    """Regression: invalid IP should be rejected and nmap should not run (no shell injection)."""
    from introduction import mitre

    # Arrange
    popen = mocker.patch.object(mitre.subprocess, "Popen", autospec=True)

    req = _make_post_request("127.0.0.1; rm -rf /")

    # Act / Assert
    with pytest.raises(Exception):
        # Depending on patch variant, code may raise ValueError or return JsonResponse(400).
        # We primarily assert it does not attempt to spawn a process.
        mitre.mitre_lab_17_api(req)

    popen.assert_not_called()
