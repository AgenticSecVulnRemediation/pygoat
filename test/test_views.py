import os

import pytest
from django.test import RequestFactory

from introduction.views import ssrf_lab


def test_ssrf_lab_rejects_absolute_path(mocker):
    rf = RequestFactory()
    request = rf.post('/ssrf/lab', data={'blog': '/etc/passwd'})
    request.user = type('U', (), {'is_authenticated': True})()

    mocker.patch('introduction.views.render', side_effect=lambda _r, _t, ctx=None: ctx)

    ctx = ssrf_lab(request)
    assert ctx['blog'] == 'Invalid file path.'


def test_ssrf_lab_rejects_parent_dir_traversal(mocker):
    rf = RequestFactory()
    request = rf.post('/ssrf/lab', data={'blog': '../secret.txt'})
    request.user = type('U', (), {'is_authenticated': True})()

    mocker.patch('introduction.views.render', side_effect=lambda _r, _t, ctx=None: ctx)

    ctx = ssrf_lab(request)
    assert ctx['blog'] == 'Invalid file path.'
