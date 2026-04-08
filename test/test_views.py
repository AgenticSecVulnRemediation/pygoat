import os
import types
import pytest


# Assumption: Django app module path is introduction.views
# These tests focus only on the SSRF lab path traversal fix in ssrf_lab.


def _make_request(user_authenticated=True, method="POST", blog_value="readme.txt"):
    user = types.SimpleNamespace(is_authenticated=user_authenticated)
    return types.SimpleNamespace(
        user=user,
        method=method,
        POST={"blog": blog_value},
    )


def test_ssrf_lab_rejects_absolute_path(monkeypatch):
    import introduction.views as views

    # Arrange: authenticated user, POST with absolute path
    request = _make_request(blog_value="/etc/passwd")

    # Patch render to observe context without Django
    def fake_render(_request, template, context=None):
        return {"template": template, "context": context or {}}

    monkeypatch.setattr(views, "render", fake_render)

    # Act
    result = views.ssrf_lab(request)

    # Assert
    assert result["template"].endswith("Lab/ssrf/ssrf_lab.html")
    assert result["context"]["blog"] == "Invalid file path provided."


@pytest.mark.parametrize("payload", [
    "../secrets.txt",
    "..\\secrets.txt",
    "subdir/file.txt",
    "subdir\\file.txt",
])
def test_ssrf_lab_rejects_traversal_or_path_separators(monkeypatch, payload):
    import introduction.views as views

    request = _make_request(blog_value=payload)

    def fake_render(_request, template, context=None):
        return {"template": template, "context": context or {}}

    monkeypatch.setattr(views, "render", fake_render)

    result = views.ssrf_lab(request)

    assert result["context"]["blog"] == "Invalid file path provided."


def test_ssrf_lab_allows_simple_filename_and_attempts_open(monkeypatch):
    import introduction.views as views

    request = _make_request(blog_value="blog.txt")

    opened = {"path": None}

    class DummyFile:
        def read(self):
            return "hello"

    def fake_open(path, mode):
        opened["path"] = path
        assert mode == "r"
        return DummyFile()

    def fake_render(_request, template, context=None):
        return {"template": template, "context": context or {}}

    monkeypatch.setattr(views, "render", fake_render)
    monkeypatch.setattr(views, "open", fake_open, raising=False)

    # Act
    result = views.ssrf_lab(request)

    # Assert: open called with a joined path ending in blog.txt
    assert opened["path"] is not None
    assert opened["path"].endswith(os.sep + "blog.txt") or opened["path"].endswith("/blog.txt")
    assert result["context"]["blog"] == "hello"
