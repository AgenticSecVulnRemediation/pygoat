# Assumption: repository uses pytest; Django is installed in CI.


def test_a9_lab_uses_yaml_safe_load(monkeypatch):
    """Delta: a9_lab switched from yaml.load(..., yaml.Loader) to yaml.safe_load."""
    from introduction import views

    called = {"safe": 0, "load": 0}

    def _fake_safe_load(_file):
        called["safe"] += 1
        return {"ok": True}

    def _fake_load(_file, _loader=None):
        called["load"] += 1
        return {"bad": True}

    monkeypatch.setattr(views.yaml, "safe_load", _fake_safe_load)
    monkeypatch.setattr(views.yaml, "load", _fake_load)

    # Avoid template dependency
    monkeypatch.setattr(views, "render", lambda request, tpl, ctx=None: ctx or {})

    class _Req:
        user = type("U", (), {"is_authenticated": True})()
        method = "POST"
        FILES = {"file": object()}

    result = views.a9_lab(_Req())

    assert called["safe"] == 1
    assert called["load"] == 0
    assert result.get("data") == {"ok": True}
