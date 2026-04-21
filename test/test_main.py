import os

# Assumption: module path is importable as introduction.playground.ssrf.main
from introduction.playground.ssrf import main


def test_ssrf_lab_rejects_directory_traversal_and_does_not_open(monkeypatch):
    # Arrange
    def fail_open(*args, **kwargs):
        raise AssertionError("open() must not be called for traversal path")

    monkeypatch.setattr(main, "open", fail_open, raising=False)

    # Act
    out = main.ssrf_lab("../secrets.txt")

    # Assert
    assert out == {"blog": "No blog found"}


def test_ssrf_lab_rejects_absolute_path_and_does_not_open(monkeypatch):
    # Arrange
    def fail_open(*args, **kwargs):
        raise AssertionError("open() must not be called for absolute path")

    monkeypatch.setattr(main, "open", fail_open, raising=False)

    # Act
    out = main.ssrf_lab("/etc/passwd")

    # Assert
    assert out == {"blog": "No blog found"}
