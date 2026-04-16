import os
import types

import pytest


@pytest.mark.django_db
def test_ssrf_lab_rejects_traversal_path_before_open(monkeypatch, mocker):
    """Delta behavior: block '..' and abs paths and enforce base dir containment."""

    from introduction import views

    open_spy = mocker.patch('builtins.open', autospec=True)

    request = types.SimpleNamespace(
        user=types.SimpleNamespace(is_authenticated=True),
        method='POST',
        POST={'blog': '../secret.txt'},
    )

    response = views.ssrf_lab(request)

    # render() returns HttpResponse
    assert hasattr(response, 'status_code')
    assert response.status_code == 200
    open_spy.assert_not_called()


@pytest.mark.django_db
def test_ssrf_lab_rejects_absolute_path_before_open(mocker):
    from introduction import views

    open_spy = mocker.patch('builtins.open', autospec=True)

    request = types.SimpleNamespace(
        user=types.SimpleNamespace(is_authenticated=True),
        method='POST',
        POST={'blog': os.path.abspath('/etc/passwd')},
    )

    response = views.ssrf_lab(request)

    assert response.status_code == 200
    open_spy.assert_not_called()
