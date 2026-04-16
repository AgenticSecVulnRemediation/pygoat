import builtins
import os
from types import SimpleNamespace


def test_ssrf_lab_rejects_traversal_and_does_not_open(monkeypatch):
    from introduction import views

    def open_fail(*args, **kwargs):
        raise AssertionError("open() should not be called for traversal attempt")

    monkeypatch.setattr(builtins, "open", open_fail)

    request = SimpleNamespace(
        user=SimpleNamespace(is_authenticated=True),
        method="POST",
        POST={"blog": "../secret.txt"},
    )

    resp = views.ssrf_lab(request)

    assert b"Invalid file name provided" in resp.content


def test_ssrf_lab_rejects_absolute_path_and_does_not_open(monkeypatch, tmp_path):
    from introduction import views

    def open_fail(*args, **kwargs):
        raise AssertionError("open() should not be called for absolute path")

    monkeypatch.setattr(builtins, "open", open_fail)

    request = SimpleNamespace(
        user=SimpleNamespace(is_authenticated=True),
        method="POST",
        POST={"blog": os.path.abspath("/etc/passwd")},
    )

    resp = views.ssrf_lab(request)

    assert b"Invalid file name provided" in resp.content
