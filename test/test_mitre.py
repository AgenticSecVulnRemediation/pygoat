import re
import types

import pytest


@pytest.fixture
def mitre_module(monkeypatch):
    """Import introduction.mitre with external deps stubbed."""
    # Provide minimal stubs for Django imports used in module import.
    django_http = types.SimpleNamespace(
        HttpResponse=lambda content, status=200: {"content": content, "status": status},
        HttpResponseBadRequest=lambda *a, **k: {"status": 400},
        JsonResponse=lambda data: data,
    )
    django_shortcuts = types.SimpleNamespace(redirect=lambda url: {"redirect": url}, render=lambda *a, **k: {"render": True})
    csrf = types.SimpleNamespace(csrf_exempt=lambda f: f)

    monkeypatch.setitem(__import__('sys').modules, 'django.http', django_http)
    monkeypatch.setitem(__import__('sys').modules, 'django.shortcuts', django_shortcuts)
    monkeypatch.setitem(__import__('sys').modules, 'django.views.decorators.csrf', csrf)

    # Patch project-level imports
    fake_models = types.SimpleNamespace(CSRF_user_tbl=types.SimpleNamespace(objects=types.SimpleNamespace(filter=lambda **k: [])))
    monkeypatch.setitem(__import__('sys').modules, 'introduction.models', fake_models)

    fake_views = types.SimpleNamespace(authentication_decorator=lambda f: f)
    monkeypatch.setitem(__import__('sys').modules, 'introduction.views', fake_views)

    import importlib

    return importlib.import_module('introduction.mitre')


def test_mitre_lab_17_api_rejects_non_ipv4_and_does_not_execute_command(mitre_module, monkeypatch):
    # Arrange
    class Req:
        method = 'POST'
        POST = {'ip': '127.0.0.1; rm -rf /'}

    called = {"count": 0}

    def fake_command_out(cmd):
        called["count"] += 1
        return (b'', b'')

    monkeypatch.setattr(mitre_module, 'command_out', fake_command_out)

    # Act
    resp = mitre_module.mitre_lab_17_api(Req())

    # Assert: invalid IP returns 400 and command_out not invoked
    assert resp["status"] == 400
    assert "Invalid IP" in resp["content"]
    assert called["count"] == 0


def test_command_out_uses_popen_without_shell(mitre_module, monkeypatch):
    # Arrange
    popen_calls = {}

    class FakePopen:
        def __init__(self, command, stdout=None, stderr=None, shell=False):
            popen_calls['command'] = command
            popen_calls['shell'] = shell
            popen_calls['stdout'] = stdout
            popen_calls['stderr'] = stderr

        def communicate(self):
            return (b'out', b'err')

    monkeypatch.setattr(mitre_module.subprocess, 'Popen', FakePopen)

    # Act
    out, err = mitre_module.command_out(['nmap', '127.0.0.1'])

    # Assert
    assert out == b'out'
    assert err == b'err'
    assert popen_calls['shell'] is False
    assert popen_calls['command'] == ['nmap', '127.0.0.1']
