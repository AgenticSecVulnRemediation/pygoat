import pytest


def test_playground_ssrf_lab_rejects_absolute_and_parent_paths(monkeypatch):
    """Delta test: playground ssrf_lab rejects abs paths and '..' traversal."""

    from introduction.playground.ssrf import main

    def _boom(*args, **kwargs):
        raise AssertionError("open() should not be called for invalid paths")

    monkeypatch.setattr(main, "open", _boom, raising=False)

    assert "Invalid file path provided" in main.ssrf_lab("../secret.txt")["blog"]
    assert "Invalid file path provided" in main.ssrf_lab("/etc/passwd")["blog"]


def test_playground_ssrf_lab_allows_normal_relative_file(monkeypatch, tmp_path):
    """Delta test: normal relative path still works."""

    from introduction.playground.ssrf import main

    # create a fake file under the module dir by stubbing os.path.dirname to tmp_path
    monkeypatch.setattr(main.os.path, "dirname", lambda *_: str(tmp_path))

    p = tmp_path / "blog.txt"
    p.write_text("OK")

    assert main.ssrf_lab("blog.txt") == {"blog": "OK"}
