import io

import pytest


def test_a9_lab_uses_yaml_safe_load(monkeypatch):
    # Import inside test so monkeypatching affects module usage consistently
    from introduction import views

    called = {}

    def fake_safe_load(file_obj):
        called["used"] = True
        # ensure file-like object is passed through
        assert hasattr(file_obj, "read")
        return {"ok": True}

    def fake_load(*args, **kwargs):
        raise AssertionError("yaml.load should not be used")

    monkeypatch.setattr(views.yaml, "safe_load", fake_safe_load)
    monkeypatch.setattr(views.yaml, "load", fake_load)

    class DummyUser:
        is_authenticated = True

    class DummyReq:
        method = "POST"
        user = DummyUser()
        FILES = {"file": io.BytesIO(b"a: 1")}

    resp = views.a9_lab(DummyReq())

    assert called.get("used") is True
    assert resp.status_code == 200
