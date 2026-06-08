import pytest

# Assumption: Django view module is importable as introduction.views in this repo layout.
from introduction import views


class _DummyUser:
    is_authenticated = True


class _DummyRequest:
    def __init__(self, url: str):
        self.method = "POST"
        self.user = _DummyUser()
        self.POST = {"url": url}


def test_ssrf_lab2_rejects_localhost_urls(mocker):
    """Regression test for SSRF fix: localhost/127.0.0.1 must be blocked before requests.get is called."""
    # Arrange
    mock_render = mocker.patch.object(views, "render", autospec=True)
    mock_requests_get = mocker.patch.object(views.requests, "get", autospec=True)
    req = _DummyRequest("http://127.0.0.1/admin")

    # Act
    views.ssrf_lab2(req)

    # Assert
    mock_requests_get.assert_not_called()
    mock_render.assert_called_once()
    # Render should be invoked with an error indicating URL is invalid/disallowed
    assert mock_render.call_args.args[2]["error"] == "Invalid or disallowed URL"
