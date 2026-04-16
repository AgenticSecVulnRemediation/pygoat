import types

import pytest


@pytest.mark.django_db
def test_xss_lab_2_template_no_longer_marks_username_safe(client, settings):
    """Delta behavior: template removed `|safe` so HTML is escaped by Django.

    Uses Django test client; assumes URL /xssL2 maps to views.xss_lab2.
    """

    # If the project uses login-required middleware, this may need authentication;
    # keeping test minimal by directly calling view if client requires auth.
    from django.test import RequestFactory
    from introduction.views import xss_lab2

    rf = RequestFactory()
    request = rf.post('/xssL2', data={'username': '<img src=x onerror=alert(1)>'})
    request.user = types.SimpleNamespace(is_authenticated=True)

    response = xss_lab2(request)
    content = response.content.decode('utf-8')

    assert '<img src=x onerror=alert(1)>' not in content
    assert '&lt;img src=x onerror=alert(1)&gt;' in content
