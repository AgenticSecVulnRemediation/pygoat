import pytest


def test_ssrf_lab_blocks_absolute_or_parent_paths(client, django_user_model):
    """Delta test: ssrf_lab now blocks abs paths or '..' traversal."""
    user = django_user_model.objects.create_user(username='u2', password='p')
    client.force_login(user)

    # Attempt traversal; should render with safe error message.
    resp = client.post('/ssrf/lab', data={'blog': '../settings.py'})
    assert resp.status_code == 200
    assert b'Invalid file path provided' in resp.content
