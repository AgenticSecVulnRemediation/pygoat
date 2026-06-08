import pytest


def test_mitre_lab_17_api_rejects_invalid_ip(client):
    """Delta test for command injection fix:

    mitre_lab_17_api now validates the IP using ipaddress.ip_address and returns 400
    for invalid values.

    Note: This test assumes a Django test client fixture named `client` exists.
    If not, replace with Django's built-in client fixture.
    """
    # Invalid IP that previously could be concatenated into shell command
    resp = client.post('/mitre/17/lab/api', data={'ip': '127.0.0.1; whoami'})
    assert resp.status_code == 400
    assert b'Invalid IP address' in resp.content
