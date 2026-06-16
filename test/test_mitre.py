import subprocess
import pytest
from django.test import RequestFactory

# Import the view function under test
from introduction.mitre import mitre_lab_17_api


@pytest.mark.django_db
def test_mitre_lab_17_api_rejects_invalid_ipv4_returns_400():
    # Arrange
    rf = RequestFactory()
    request = rf.post('/mitre/17/lab/api', data={'ip': '127.0.0.1; rm -rf /'})

    # Act
    response = mitre_lab_17_api(request)

    # Assert
    assert response.status_code == 400
    assert b'Invalid IP address' in response.content


@pytest.mark.django_db
def test_mitre_lab_17_api_valid_ipv4_uses_subprocess_without_shell(monkeypatch):
    # Arrange
    rf = RequestFactory()
    request = rf.post('/mitre/17/lab/api', data={'ip': '127.0.0.1'})

    captured = {}

    class DummyProc:
        def __init__(self, args, **kwargs):
            captured['args'] = args
            captured['kwargs'] = kwargs

        def communicate(self):
            # Enough output to satisfy regex in the view
            out = b"STATE SERVICE\n\n80/tcp open http\n"
            err = b""
            return out, err

    def fake_popen(args, **kwargs):
        return DummyProc(args, **kwargs)

    monkeypatch.setattr(subprocess, 'Popen', fake_popen)

    # Act
    response = mitre_lab_17_api(request)

    # Assert
    assert response.status_code == 200
    assert captured['args'] == ['nmap', '127.0.0.1']
    # The hardened code should not pass shell=True
    assert 'shell' not in captured['kwargs']
