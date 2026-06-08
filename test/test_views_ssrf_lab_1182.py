import os
import types
import pytest

import introduction.views as views


def test_ssrf_lab_blocks_absolute_paths(monkeypatch):
    class _Req:
        method = 'POST'
        user = types.SimpleNamespace(is_authenticated=True)
        POST = {'blog': '/etc/passwd'}

    monkeypatch.setattr(views, 'render', lambda request, template, context=None: {'template': template, 'context': context})

    resp = views.ssrf_lab(_Req())
    assert resp['context']['blog'] == 'Invalid file path'


def test_ssrf_lab_blocks_parent_traversal(monkeypatch):
    class _Req:
        method = 'POST'
        user = types.SimpleNamespace(is_authenticated=True)
        POST = {'blog': '../secrets.txt'}

    monkeypatch.setattr(views, 'render', lambda request, template, context=None: {'template': template, 'context': context})

    resp = views.ssrf_lab(_Req())
    assert resp['context']['blog'] == 'Invalid file path'
