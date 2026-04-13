import pytest


def test_ssrf_lab_rejects_absolute_paths(rf, tmp_path):
    """Delta test: ssrf_lab must reject absolute paths before joining/opening."""

    import introduction.views as views

    request = rf.post('/ssrf', data={'blog': str(tmp_path / 'secret.txt')})
    request.user = type('U', (), {'is_authenticated': True})()

    response = views.ssrf_lab(request)
    assert 'No blog found' in response.content.decode('utf-8')


def test_ssrf_lab_rejects_dotdot_paths(rf):
    """Delta test: ssrf_lab must reject path traversal via '..' segments."""

    import introduction.views as views

    request = rf.post('/ssrf', data={'blog': '../secrets.txt'})
    request.user = type('U', (), {'is_authenticated': True})()

    response = views.ssrf_lab(request)
    assert 'No blog found' in response.content.decode('utf-8')
