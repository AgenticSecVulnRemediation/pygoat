import pytest


def test_cmd_lab_validates_domain_and_blocks_shell_metacharacters(client, django_user_model):
    """Delta test: cmd_lab now validates domain and should reject injection characters.

    It now raises ValueError on invalid domains; we assert a non-200 response.

    Assumptions:
    - A Django test client fixture named `client` exists.
    - Auth is required; we create a user and force login.
    """
    user = django_user_model.objects.create_user(username='u', password='p')
    client.force_login(user)

    resp = client.post('/cmd/lab', data={'domain': 'example.com;whoami', 'os': 'linux'})

    # Depending on Django settings, ValueError may translate to 400 or 500.
    assert resp.status_code != 200
