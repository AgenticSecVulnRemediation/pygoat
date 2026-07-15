import pytest
from django.http import HttpResponseBadRequest


@pytest.fixture(autouse=True)
def _mock_mitre_module_dependencies(monkeypatch):
    """Mock all external dependencies used by introduction.mitre.

    We mock Django + project modules to keep the test unit-scoped and deterministic.
    """
    # Import inside fixture to ensure monkeypatch applies before use in tests
    import introduction.mitre as mitre

    # Ensure decorators are no-ops for unit testing
    monkeypatch.setattr(mitre, "authentication_decorator", lambda f: f, raising=False)

    # csrf_exempt decorator no-op (if imported)
    try:
        monkeypatch.setattr(mitre, "csrf_exempt", lambda f: f, raising=False)
    except Exception:
        pass

    # Avoid touching database models
    monkeypatch.setattr(mitre, "CSRF_user_tbl", object(), raising=False)


class _FakePost:
    def __init__(self, values):
        self._values = values

    def get(self, k, default=None):
        return self._values.get(k, default)


class _FakeRequest:
    def __init__(self, method="POST", post=None):
        self.method = method
        self.POST = _FakePost(post or {})


def test_mitre_lab_17_api_with_invalid_ip_returns_400(monkeypatch):
    import introduction.mitre as mitre

    # Arrange: make sure nmap is never invoked for invalid input
    called = {"value": False}

    def _boom(_cmd):
        called["value"] = True
        raise AssertionError("command_out should not be called for invalid IP")

    monkeypatch.setattr(mitre, "command_out", _boom, raising=True)

    req = _FakeRequest(post={"ip": "127.0.0.1; rm -rf /"})

    # Act
    resp = mitre.mitre_lab_17_api(req)

    # Assert
    assert isinstance(resp, HttpResponseBadRequest)
    assert resp.status_code == 400
    assert called["value"] is False


def test_mitre_lab_17_api_with_valid_ip_calls_command_out_with_list(monkeypatch):
    import introduction.mitre as mitre

    # Arrange
    observed = {"cmd": None}

    def _fake_command_out(cmd):
        observed["cmd"] = cmd
        # Return output that satisfies the regex parsing in the view.
        stdout = b"Some header\nSTATE SERVICE\n\n22/tcp open ssh\n"
        stderr = b""
        return stdout, stderr

    monkeypatch.setattr(mitre, "command_out", _fake_command_out, raising=True)

    req = _FakeRequest(post={"ip": "127.0.0.1"})

    # Act
    resp = mitre.mitre_lab_17_api(req)

    # Assert: ensure command is not a string (no shell concatenation), but argv list
    assert observed["cmd"] == ["nmap", "127.0.0.1"]
    # JsonResponse-like object has content bytes; avoid Django test client by checking attributes defensively
    assert getattr(resp, "status_code", None) == 200
