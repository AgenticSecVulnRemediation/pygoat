import pytest


def test_cmd_lab_rejects_domain_with_shell_metacharacters(monkeypatch):
    """Delta behavior: invalid domain should be rejected before subprocess is invoked."""

    import introduction.views as views

    # Patch render to return just the context for assertion
    def fake_render(request, template, context=None):
        return {"template": template, "context": context or {}}

    monkeypatch.setattr(views, "render", fake_render)

    # If subprocess.Popen is called, the fix didn't short-circuit properly
    monkeypatch.setattr(views.subprocess, "Popen", lambda *a, **k: (_ for _ in ()).throw(AssertionError("Popen should not be called")))

    class User:
        is_authenticated = True

    class Request:
        user = User()
        method = "POST"

        def __init__(self):
            self.POST = {"domain": "example.com;cat /etc/passwd", "os": "linux"}

    resp = views.cmd_lab(Request())

    assert resp["template"].endswith("Lab/CMD/cmd_lab.html")
    assert resp["context"]["output"] == "Invalid domain input."


def test_cmd_lab_rejects_invalid_os(monkeypatch):
    """Delta behavior: invalid os value should be rejected before subprocess is invoked."""

    import introduction.views as views

    def fake_render(request, template, context=None):
        return {"template": template, "context": context or {}}

    monkeypatch.setattr(views, "render", fake_render)
    monkeypatch.setattr(views.subprocess, "Popen", lambda *a, **k: (_ for _ in ()).throw(AssertionError("Popen should not be called")))

    class User:
        is_authenticated = True

    class Request:
        user = User()
        method = "POST"

        def __init__(self):
            self.POST = {"domain": "example.com", "os": "linux;rm -rf /"}

    resp = views.cmd_lab(Request())

    assert resp["template"].endswith("Lab/CMD/cmd_lab.html")
    assert resp["context"]["output"] == "Invalid OS specified."


def test_cmd_lab_invokes_subprocess_with_shell_false_and_arg_list(monkeypatch):
    """Delta behavior: command is passed as list and shell=True is removed."""

    import introduction.views as views

    def fake_render(request, template, context=None):
        return {"template": template, "context": context or {}}

    monkeypatch.setattr(views, "render", fake_render)

    captured = {}

    class FakeProc:
        def communicate(self):
            return (b"OK", b"")

    def fake_popen(cmd, **kwargs):
        captured["cmd"] = cmd
        captured["kwargs"] = kwargs
        return FakeProc()

    monkeypatch.setattr(views.subprocess, "Popen", fake_popen)

    class User:
        is_authenticated = True

    class Request:
        user = User()
        method = "POST"

        def __init__(self):
            self.POST = {"domain": "example.com", "os": "win"}

    resp = views.cmd_lab(Request())

    assert captured["cmd"] == ["nslookup", "example.com"]
    assert "shell" not in captured["kwargs"], "shell kwarg should not be set (defaults to False)"
    assert resp["template"].endswith("Lab/CMD/cmd_lab.html")
