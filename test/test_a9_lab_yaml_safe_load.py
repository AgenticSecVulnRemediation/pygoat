import pytest


def test_a9_lab_uses_yaml_safe_load(monkeypatch):
    """Delta test: yaml.safe_load must be used; yaml.load should not be called."""

    from introduction import views

    # If the vulnerable yaml.load is called, fail.
    def boom(*args, **kwargs):
        raise AssertionError("yaml.load should not be used")

    monkeypatch.setattr(views.yaml, "load", boom)

    captured = {}

    def fake_safe_load(f):
        captured["called"] = True
        return {"ok": True}

    monkeypatch.setattr(views.yaml, "safe_load", fake_safe_load)

    class DummyUser:
        is_authenticated = True

    class DummyReq:
        method = "POST"
        user = DummyUser()
        FILES = {"file": object()}

    resp = views.a9_lab(DummyReq())
    assert captured.get("called") is True
    assert b"ok" in resp.content
