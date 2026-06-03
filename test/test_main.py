import os
import types

from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_absolute_path_and_does_not_read(tmp_path, monkeypatch):
    # Arrange: create a fake "blog" file outside the module directory
    secret_file = tmp_path / "secret.txt"
    secret_file.write_text("TOPSECRET")

    # Defensive: if the vulnerable path were still allowed, open() would be called.
    def fail_open(*args, **kwargs):
        raise AssertionError("open() should not be called for invalid file paths")

    monkeypatch.setattr("builtins.open", fail_open)

    # Act
    result = ssrf_lab(str(secret_file))

    # Assert: function must not expose file contents; it should return default message
    assert result == {"blog": "No blog found"}


def test_ssrf_lab_rejects_directory_traversal_and_does_not_read(monkeypatch):
    # Arrange
    def fail_open(*args, **kwargs):
        raise AssertionError("open() should not be called for traversal paths")

    monkeypatch.setattr("builtins.open", fail_open)

    # Act
    result = ssrf_lab("../etc/passwd")

    # Assert
    assert result == {"blog": "No blog found"}
