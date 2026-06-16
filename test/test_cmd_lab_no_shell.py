import os
import re
import subprocess

import pytest


@pytest.mark.django_db
def test_cmd_lab_uses_subprocess_without_shell_and_list_args(monkeypatch):
    """Delta test for PR 1442: cmd_lab should call subprocess.Popen with shell=False and args list.

    Previously vulnerable behavior: shell=True with a formatted string command could allow shell injection.
    """
    # Import inside test to avoid Django setup at import time in some runners
    import introduction.views as views

    class DummyUser:
        is_authenticated = True

    class DummyRequest:
        method = "POST"
        user = DummyUser()
        POST = {"domain": "example.com; echo pwned", "os": "win"}

    captured = {}

    class DummyProcess:
        def communicate(self):
            return (b"ok", b"")

    def fake_popen(args, shell, stdout, stderr):
        captured["args"] = args
        captured["shell"] = shell
        captured["stdout"] = stdout
        captured["stderr"] = stderr
        return DummyProcess()

    def fake_render(request, template, context=None):
        # Ensure view returns and uses output
        return {"template": template, "context": context or {}}

    monkeypatch.setattr(subprocess, "Popen", fake_popen)
    monkeypatch.setattr(views, "render", fake_render)

    resp = views.cmd_lab(DummyRequest())

    assert captured["shell"] is False
    assert isinstance(captured["args"], list)
    # ensure the command is not a formatted string passed to shell
    assert captured["args"][0] == "nslookup"
    # domain should be sanitized to strip protocol/www prefix; injection chars should be treated as literal arg
    assert captured["args"][1].startswith("example.com")
    assert resp["template"].endswith("cmd_lab.html")
    assert "output" in resp["context"]
