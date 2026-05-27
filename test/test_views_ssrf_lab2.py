import pytest


@pytest.mark.django_db
def test_ssrf_lab2_blocks_unauthorized_scheme(mocker):
    """Regression: SSRF fix blocks non-http(s) schemes."""
    from introduction import views

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        method = "POST"
        user = DummyUser()
        POST = {"url": "file:///etc/passwd"}

    get_mock = mocker.patch.object(views.requests, "get")

    response = views.ssrf_lab2(DummyRequest())

    assert response.status_code == 200
    # Must not make outbound request
    get_mock.assert_not_called()


@pytest.mark.django_db
def test_ssrf_lab2_blocks_unauthorized_host(mocker):
    """Regression: SSRF fix blocks hosts not on allowlist."""
    from introduction import views

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        method = "POST"
        user = DummyUser()
        POST = {"url": "https://evil.com/"}

    get_mock = mocker.patch.object(views.requests, "get")

    response = views.ssrf_lab2(DummyRequest())

    assert response.status_code == 200
    get_mock.assert_not_called()


@pytest.mark.django_db
def test_ssrf_lab2_allows_http_example_dot_com(mocker):
    """Regression: allowlisted host and scheme proceed to requests.get."""
    from introduction import views

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        method = "POST"
        user = DummyUser()
        POST = {"url": "https://example.com/"}

    class Resp:
        content = b"ok"

    get_mock = mocker.patch.object(views.requests, "get", return_value=Resp())

    response = views.ssrf_lab2(DummyRequest())

    assert response.status_code == 200
    get_mock.assert_called_once_with("https://example.com/")
