# Assumptions:
# - Repository uses pytest
# - Django is installed and configured for unit tests
# - The views module is importable as introduction.views

import pytest


def test_ssrf_lab_rejects_non_allowlisted_blog_key(monkeypatch):
    """The fix enforces an allowlist for blog selection to prevent arbitrary file read."""
    import introduction.views as views

    class _User:
        is_authenticated = True

    class _Request:
        user = _User()
        method = "POST"
        POST = {"blog": "../../etc/passwd"}

    def fake_render(_request, _template, context=None, *args, **kwargs):
        return {"template": _template, "context": context or {}}

    monkeypatch.setattr(views, "render", fake_render)

    def explode_open(*args, **kwargs):
        raise AssertionError("open() should not be called for disallowed blog keys")

    monkeypatch.setattr(views, "open", explode_open, raising=True)

    result = views.ssrf_lab(_Request())

    assert result["template"] == "Lab/ssrf/ssrf_lab.html"
    assert result["context"]["blog"] == "No blog found"


def test_ssrf_lab_reads_only_allowlisted_file_for_blog_key(monkeypatch):
    """When a valid key is provided, the corresponding safe file is read."""
    import introduction.views as views

    class _User:
        is_authenticated = True

    class _Request:
        user = _User()
        method = "POST"
        POST = {"blog": "blog1"}

    def fake_render(_request, _template, context=None, *args, **kwargs):
        return {"template": _template, "context": context or {}}

    monkeypatch.setattr(views, "render", fake_render)

    opened = {"path": None}

    class _FakeFile:
        def read(self):
            return "SAFE CONTENT"

    def fake_open(path, mode="r", *args, **kwargs):
        opened["path"] = path
        return _FakeFile()

    monkeypatch.setattr(views, "open", fake_open, raising=True)

    result = views.ssrf_lab(_Request())

    assert opened["path"].endswith("safe_file1.txt")
    assert result["template"] == "Lab/ssrf/ssrf_lab.html"
    assert result["context"]["blog"] == "SAFE CONTENT"
