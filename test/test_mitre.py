import introduction.mitre as mitre


class _FakeRequest:
    def __init__(self, ip: str):
        self.method = "POST"
        self.POST = {"ip": ip}


def test_mitre_lab_17_api_rejects_invalid_ip_returns_bad_request(monkeypatch):
    """Regression: rejects invalid IP (prevents command injection via concatenation)."""
    # Arrange: avoid auth wrapper blocking this unit test
    monkeypatch.setattr(mitre, "authentication_decorator", lambda f: f)

    # Ensure no subprocess execution happens
    monkeypatch.setattr(mitre, "command_out", lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("command_out should not be called")))

    # Act
    resp = mitre.mitre_lab_17_api(_FakeRequest("8.8.8.8 && whoami"))

    # Assert
    # HttpResponseBadRequest sets status_code to 400
    assert getattr(resp, "status_code", None) == 400
