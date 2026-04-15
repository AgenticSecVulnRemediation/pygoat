import os

import introduction.playground.ssrf.main as ssrf_main


def test_ssrf_lab_rejects_path_traversal_outside_base_dir(tmp_path, monkeypatch):
    # Arrange: point the module's __file__ into a temp directory so base_dir is controlled.
    monkeypatch.setattr(ssrf_main, "__file__", str(tmp_path / "main.py"))

    outside_target = tmp_path.parent / "outside.txt"
    outside_target.write_text("secret", encoding="utf-8")

    traversal = os.path.join("..", outside_target.name)

    # Act
    result = ssrf_main.ssrf_lab(traversal)

    # Assert
    assert result == {"blog": "No blog found"}


def test_ssrf_lab_allows_reading_file_within_base_dir(tmp_path, monkeypatch):
    # Arrange
    monkeypatch.setattr(ssrf_main, "__file__", str(tmp_path / "main.py"))
    inside = tmp_path / "blog.txt"
    inside.write_text("hello", encoding="utf-8")

    # Act
    result = ssrf_main.ssrf_lab("blog.txt")

    # Assert
    assert result == {"blog": "hello"}
