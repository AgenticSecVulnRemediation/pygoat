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


def test_ssrf_lab_blocks_path_traversal_and_does_not_open(mocker):
    """After the fix, traversal sequences/absolute paths should return a safe response and not read files."""
    from introduction import views

    open_spy = mocker.patch('builtins.open', autospec=True)

    req = _Request(blog_value='../etc/passwd')
    resp = views.ssrf_lab(req)

    assert isinstance(resp, HttpResponse)
    assert resp.status_code == 200
    open_spy.assert_not_called()
