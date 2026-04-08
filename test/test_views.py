import os
import types
import pytest


# Assumption: Django app module path is introduction.views
# Tests focus only on the canonicalization + base_dir containment check in ssrf_lab.


def _make_request(blog_value, user_authenticated=True, method="POST"):
    user = types.SimpleNamespace(is_authenticated=user_authenticated)
    return types.SimpleNamespace(user=user, method=method, POST={"blog": blog_value})


def test_ssrf_lab_blocks_traversal_after_realpath(monkeypatch):
    import introduction.views as views

    request = _make_request("../etc/passwd")

    # Make base_dir and real_path deterministic
    monkeypatch.setattr(views.os.path, 'dirname', lambda _p: '/base')
    monkeypatch.setattr(views.os.path, 'realpath', lambda p: '/base' if p == '/base' else '/etc/passwd')
    monkeypatch.setattr(views.os.path, 'join', lambda a, b: f"{a}/{b}")

    # If open is called, containment check failed
    monkeypatch.setattr(views, 'open', lambda *_a, **_k: (_ for _ in ()).throw(AssertionError('open should not be called')), raising=False)

    monkeypatch.setattr(views, 'render', lambda _r, _t, ctx=None: {"ctx": ctx or {}})

    result = views.ssrf_lab(request)

    assert result["ctx"]["blog"] == "No blog found"


def test_ssrf_lab_reads_file_within_base_dir(monkeypatch):
    import introduction.views as views

    request = _make_request("blog.txt")

    monkeypatch.setattr(views.os.path, 'dirname', lambda _p: '/base')
    monkeypatch.setattr(views.os.path, 'realpath', lambda p: '/base' if p == '/base' else '/base/blog.txt')
    monkeypatch.setattr(views.os.path, 'join', lambda a, b: f"{a}/{b}")

    class DummyFile:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return 'ok'

    monkeypatch.setattr(views, 'open', lambda *_a, **_k: DummyFile(), raising=False)
    monkeypatch.setattr(views, 'render', lambda _r, _t, ctx=None: {"ctx": ctx or {}})

    result = views.ssrf_lab(request)

    assert result["ctx"]["blog"] == "ok"
