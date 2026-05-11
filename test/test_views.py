import builtins


def test_ssrf_lab_rejects_invalid_file_paths(monkeypatch):
    """Delta: ssrf_lab now rejects absolute and parent-traversal paths."""
    from introduction import views

    def _fake_render(_request, _tpl, ctx=None):
        return ctx or {}

    monkeypatch.setattr(views, "render", _fake_render)

    # Fail if open() would be called for invalid paths.
    monkeypatch.setattr(builtins, "open", lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("open called")))

    class _Req:
        user = type("U", (), {"is_authenticated": True})()
        method = "POST"
        POST = {"blog": "../x.txt"}

    res = views.ssrf_lab(_Req())
    assert res.get("blog") == "Invalid file path"
