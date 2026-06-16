import pytest


def test_xss_lab_2_username_not_marked_safe_renders_escaped(client, django_user_model):
    """Regression test for template change: removed '|safe' so user input is escaped."""
    user = django_user_model.objects.create_user(username='u1', password='p1')
    client.login(username='u1', password='p1')

    payload = '<img src=x onerror=alert(1)>'

    resp = client.post('/xssL2', data={'username': payload})
    assert resp.status_code == 200

    # Should be escaped; raw payload should not appear as HTML
    content = resp.content.decode('utf-8')
    assert payload not in content
    assert '&lt;img' in content
