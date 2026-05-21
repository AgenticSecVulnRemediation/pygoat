import re

import pytest

# NOTE: The module under test lives in introduction/mitre.py and isn't a package import
# in this repo layout. We import it via sys.path manipulation for direct module import.
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import introduction.mitre as mitre  # noqa: E402


def test_mitre_lab_17_api_rejects_invalid_ip_and_does_not_invoke_subprocess(mocker):
    """Regression test for command injection fix.

    The fix validates the IP using ipaddress.ip_address and runs subprocess with shell=False
    using argument list. An invalid IP should return 400 and must not execute nmap.
    """
    # Arrange
    request = mocker.Mock()
    request.method = "POST"
    request.POST.get.side_effect = lambda k: {"ip": "1.2.3.4; rm -rf /"}.get(k)

    command_out_spy = mocker.patch.object(mitre, "command_out", autospec=True)

    # Act
    response = mitre.mitre_lab_17_api(request)

    # Assert
    assert response.status_code == 400
    assert b"Invalid IP address" in response.content
    command_out_spy.assert_not_called()
