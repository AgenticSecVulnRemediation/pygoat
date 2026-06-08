import pytest


def test_ssrf_lab2_blocks_non_allowlisted_hostname(client, django_user_model, mocker):
    """Delta test: ssrf_lab2 now enforces hostname allowlist before requests.get."""
    user = django_user_model.objects.create_user(username='u3', password='p')
    client.force_login(user)

    get_spy = mocker.patch('introduction.views.requests.get')

    resp = client.post('/ssrf/lab2', data={'url': 'http://127.0.0.1/admin'})

    assert resp.status_code == 200
    assert b'Unauthorized URL host.' in resp.content
    get_spy.assert_not_called()
