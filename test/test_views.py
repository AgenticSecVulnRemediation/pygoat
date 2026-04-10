import importlib


def test_cmd_lab_invalid_domain_returns_error_and_does_not_spawn_subprocess(monkeypatch):
    # Arrange
    views = importlib.import_module('introduction.views')

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        user = DummyUser()
        method = "POST"
        POST = {"domain": "example.com;rm -rf /", "os": "linux"}

    def fake_popen(*args, **kwargs):
        raise AssertionError("subprocess.Popen should not be called for invalid domain")

    monkeypatch.setattr(views.subprocess, "Popen", fake_popen)

    # Act
    resp = views.cmd_lab(DummyRequest())

    # Assert
    assert hasattr(resp, 'status_code')
    assert resp.status_code == 200
    # Django HttpResponse content contains rendered HTML; ensure our error message is present.
    assert b"Invalid domain format" in resp.content
