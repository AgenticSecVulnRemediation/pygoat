import json
import subprocess

import pytest


class _FakeRequest:
    def __init__(self, ip: str):
        self.method = "POST"
        self.POST = {"ip": ip}


@pytest.mark.parametrize(
    "malicious_ip",
    [
        # Attempt to smuggle shell metacharacters that would have been dangerous with shell=True
        "127.0.0.1; whoami",
        "127.0.0.1 && id",
        "127.0.0.1 | cat /etc/passwd",
    ],
)
def test_mitre_lab_17_api_rejects_non_ip_input(mocker, malicious_ip):
    """Regression test for command injection hardening.

    The patch added ipaddress.ip_address() validation and removed shell=True.
    Ensure that non-IP strings are rejected with HTTP 400 and that no subprocess is spawned.
    """

    # Import inside test so that Django isn't required at collection time in environments without it.
    from introduction import mitre

    popen_spy = mocker.patch.object(subprocess, "Popen", autospec=True)

    request = _FakeRequest(malicious_ip)
    response = mitre.mitre_lab_17_api(request)

    assert getattr(response, "status_code", None) == 400

    # Django JsonResponse stores bytes in `content`; keep assertion defensive.
    content = getattr(response, "content", b"")
    payload = json.loads(content.decode("utf-8"))
    assert payload["error"] == "Invalid IP address"

    popen_spy.assert_not_called()
