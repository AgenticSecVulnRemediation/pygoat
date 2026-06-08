import pytest
from django.http import HttpResponse

# Delta unit tests for SSRF lab file path traversal hardening in introduction.views.ssrf_lab


class _User:
    is_authenticated = True


class _Request:
    def __init__(self, blog_value: str):
        self.user = _User()
        self.method = 'POST'
        self.POST = {'blog': blog_value}


def test_ssrf_lab_rejects_absolute_path(mocker):
    """After the fix, absolute paths should not be opened (prevents arbitrary file read)."""
    from introduction import views

    open_spy = mocker.patch('builtins.open', autospec=True)

    req = _Request(blog_value='/etc/passwd')
    resp = views.ssrf_lab(req)

    assert isinstance(resp, HttpResponse)
    assert resp.status_code == 200
    # on rejection path, open must not be called
    open_spy.assert_not_called()


def test_ssrf_lab_rejects_directory_traversal(mocker):
    """After the fix, '..' traversal sequences should not be opened."""
    from introduction import views

    open_spy = mocker.patch('builtins.open', autospec=True)

    req = _Request(blog_value='../../secret.txt')
    resp = views.ssrf_lab(req)

    assert isinstance(resp, HttpResponse)
    assert resp.status_code == 200
    open_spy.assert_not_called()
