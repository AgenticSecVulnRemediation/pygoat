# Assumptions:
# - Django is available in the test environment.
# - The project uses pytest + pytest-django.

import json
import pytest
from django.test import RequestFactory


@pytest.mark.django_db
def test_mitre_lab_17_api_rejects_non_ip_input_without_shell_execution(mocker):
    """Regression for command injection fix.

    The fix:
    - validates ip with ipaddress.ip_address
    - runs subprocess with shell=False and command list ["nmap", ip]

    This test ensures invalid input returns an error and does not call subprocess.
    """
    from introduction import mitre

    popen = mocker.patch("introduction.mitre.subprocess.Popen")

    rf = RequestFactory()
    req = rf.post("/mitre/17/lab/api", data={"ip": "8.8.8.8; whoami"})

    resp = mitre.mitre_lab_17_api(req)
    assert resp.status_code == 200
    assert b"Invalid IP address" in resp.content

    popen.assert_not_called()


@pytest.mark.django_db
def test_mitre_lab_17_api_uses_shell_false_and_list_command_for_valid_ip(mocker):
    """Ensures subprocess is invoked safely for valid IP."""
    from introduction import mitre

    class _Proc:
        def communicate(self):
            # Minimal output matching expected regex in view
            res = b"STATE SERVICE\n\n80/tcp open http\n"
            err = b""
            return res, err

    popen = mocker.patch("introduction.mitre.subprocess.Popen", return_value=_Proc())

    rf = RequestFactory()
    req = rf.post("/mitre/17/lab/api", data={"ip": "127.0.0.1"})

    resp = mitre.mitre_lab_17_api(req)
    assert resp.status_code == 200

    data = json.loads(resp.content.decode("utf-8"))
    assert "ports" in data
    assert "80/tcp open http" in "\n".join(data["ports"])

    popen.assert_called_once()
    args, kwargs = popen.call_args
    assert args[0] == ["nmap", "127.0.0.1"]
    assert kwargs.get("shell") is False
