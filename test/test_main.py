import os

import introduction.playground.ssrf.main as ssrf


def test_ssrf_lab_rejects_absolute_path():
    assert ssrf.ssrf_lab("/etc/passwd") == {"blog": "No blog found"}


def test_ssrf_lab_rejects_directory_traversal():
    assert ssrf.ssrf_lab("../secrets.txt") == {"blog": "No blog found"}


def test_ssrf_lab_allows_relative_path_and_reads_file(tmp_path, monkeypatch):
    # Arrange: create a fake module dirname and a target file within it
    base_dir = tmp_path / "playground"
    base_dir.mkdir()
    target = base_dir / "blog.txt"
    target.write_text("hello", encoding="utf-8")

    monkeypatch.setattr(os.path, "dirname", lambda _: str(base_dir))

    # Act
    result = ssrf.ssrf_lab("blog.txt")

    # Assert
    assert result == {"blog": "hello"}
