import pytest


# Tests cover the SSRF hardening in ssrf_lab2 (introduction/views.py):
# enforce allowed scheme and host before requests.get.


def test_ssrf_lab2_disallowed_url_is_blocked_and_requests_not_made(mocker):
    from introduction import views

    get_mock = mocker.patch('introduction.views.requests.get', side_effect=AssertionError("requests.get must not be called"))

    class _Req:
        method = "POST"
        POST = {'url': 'http://127.0.0.1/admin'}

    resp = views.ssrf_lab2(_Req())

    assert not get_mock.called
    assert resp is not None


def test_ssrf_lab2_allowed_url_calls_requests_get(mocker):
    from introduction import views

    get_mock = mocker.patch('introduction.views.requests.get')
    get_mock.return_value.content = b"OK"

    class _Req:
        method = "POST"
        POST = {'url': 'https://example.com/'}

    resp = views.ssrf_lab2(_Req())

    get_mock.assert_called_once()
    assert resp is not None
