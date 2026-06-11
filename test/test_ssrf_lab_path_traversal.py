import os

import pytest


def test_ssrf_lab_blocks_path_traversal(monkeypatch):
    """Delta test: ssrf_lab should reject '..' and absolute paths before opening files."""

    from introduction import views

    # Ensure open isn't called for malicious paths
    def _boom(*args, **kwargs):
        raise AssertionError("open() should not be called for traversal/absolute paths")

    monkeypatch.setattr(views, "open", _boom, raising=False)

    # Dummy request/session/user
    class DummyUser:
        is_authenticated = True

    class DummyReq:
        method = "POST"
        user = DummyUser()
        POST = {"blog": "../secret.txt"}

    resp = views.ssrf_lab(DummyReq())

    # Response is a rendered template. Ensure the message is included.
    assert b"Invalid file path" in resp.content


def test_ssrf_lab_allows_relative_paths_and_reads_file(monkeypatch):
    """Delta test: normal relative paths should still be read."""

    from introduction import views

    class DummyFile:
        def read(self):
            return "BLOG"

    def fake_open(path, mode):
        # should be joined under the module directory
        assert mode == "r"
        assert not os.path.isabs(path)
        return DummyFile()

    monkeypatch.setattr(views, "open", fake_open, raising=False)

    class DummyUser:
        is_authenticated = True

    class DummyReq:
        method = "POST"
        user = DummyUser()
        POST = {"blog": "templates/blog.txt"}

    resp = views.ssrf_lab(DummyReq())
    assert b"BLOG" in resp.content
