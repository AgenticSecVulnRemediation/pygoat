import pytest

# Assumption: module is importable as introduction.views
import introduction.views as views


def test_ssrf_lab_blocks_traversal_and_does_not_open(monkeypatch):
    # Arrange
    request = type("Req", (), {})()
    request.user = type("User", (), {"is_authenticated": True})()
    request.method = "POST"
    request.POST = {"blog": "../secret.txt"}

    def boom_open(*args, **kwargs):
        raise AssertionError("open must not be called when traversal is detected")

    monkeypatch.setattr(views, "open", boom_open, raising=False)

    # Act
    resp = views.ssrf_lab(request)

    # Assert
    assert b"Invalid file path" in resp.content


def test_ssrf_lab_reads_file_via_with_open(monkeypatch):
    # Arrange
    request = type("Req", (), {})()
    request.user = type("User", (), {"is_authenticated": True})()
    request.method = "POST"
    request.POST = {"blog": "README.md"}

    class FakeFile:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return "hello"

    opened = {"path": None}

    def fake_open(path, mode):
        opened["path"] = path
        assert mode == "r"
        return FakeFile()

    monkeypatch.setattr(views, "open", fake_open, raising=False)
    # Ensure path checks succeed deterministically
    monkeypatch.setattr(views.os.path, "isabs", lambda p: False)
    monkeypatch.setattr(views.os.path, "abspath", lambda p: "/base/" + p.strip("/") if not p.startswith("/base") else p)
    monkeypatch.setattr(views.os.path, "dirname", lambda p: "/base")
    monkeypatch.setattr(views.os.path, "join", lambda a, b: a + "/" + b)

    # Act
    resp = views.ssrf_lab(request)

    # Assert
    assert b"hello" in resp.content
    assert opened["path"] is not None
