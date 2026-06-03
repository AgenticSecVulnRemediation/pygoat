import io

import introduction.views as views


class _DummyUser:
    is_authenticated = True


class _FakeRequest:
    def __init__(self, domain: str, os_value: str = "linux"):
        self.method = "POST"
        self.user = _DummyUser()
        self.POST = {"domain": domain, "os": os_value}


def test_cmd_lab_rejects_invalid_domain_and_does_not_invoke_subprocess(monkeypatch):
    """Regression: domain is now validated; injection characters should be rejected."""

    # Arrange: make render return the output context so we can assert on it
    def _fake_render(_request, _template, context=None, **_kwargs):
        return context

    monkeypatch.setattr(views, "render", _fake_render)

    # Ensure subprocess isn't called
    monkeypatch.setattr(
        views.subprocess,
        "Popen",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("Popen should not be called")),
    )

    # Act
    ctx = views.cmd_lab(_FakeRequest("example.com; cat /etc/passwd"))

    # Assert
    assert ctx["output"] == "Invalid domain"


def test_cmd_lab_uses_argv_list_and_no_shell(monkeypatch):
    """Regression: command must be argv-list and shell must not be used."""

    def _fake_render(_request, _template, context=None, **_kwargs):
        return context

    monkeypatch.setattr(views, "render", _fake_render)

    captured = {}

    class _Proc:
        def communicate(self):
            return (b"stdout", b"stderr")

    def _fake_popen(cmd, stdout=None, stderr=None, **kwargs):
        captured["cmd"] = cmd
        captured["kwargs"] = kwargs
        return _Proc()

    monkeypatch.setattr(views.subprocess, "Popen", _fake_popen)

    ctx = views.cmd_lab(_FakeRequest("example.com", os_value="linux"))

    assert captured["cmd"] == ["dig", "example.com"]
    assert "shell" not in captured["kwargs"]
    assert ctx["output"] == "stdoutstderr"
