import pytest


def test_cmd_lab_uses_shell_false_and_list_command(monkeypatch):
    """Delta behavior: command is list and subprocess.Popen is called without shell=True."""

    import introduction.views as views

    # Patch render to avoid template rendering in unit test
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
            self.POST = {"domain": "example.com", "os": "linux"}

    resp = views.cmd_lab(Request())

    assert captured["cmd"] == ["dig", "example.com"]
    assert "shell" not in captured["kwargs"], "shell kwarg should not be passed"
    assert resp["template"].endswith("Lab/CMD/cmd_lab.html")


def test_cmd_lab_invalid_domain_raises_value_error(monkeypatch):
    """Delta behavior: invalid domain now raises ValueError before invoking subprocess."""

    import introduction.views as views

    monkeypatch.setattr(views.subprocess, "Popen", lambda *a, **k: (_ for _ in ()).throw(AssertionError("Popen should not be called")))

    class User:
        is_authenticated = True

    class Request:
        user = User()
        method = "POST"

        def __init__(self):
            self.POST = {"domain": "bad.com;id", "os": "linux"}

    with pytest.raises(ValueError, match="Invalid domain"):
        views.cmd_lab(Request())
