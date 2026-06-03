import os

from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_absolute_paths(monkeypatch, tmp_path):
    """Regression: absolute paths must not be read (previously could read arbitrary files)."""
    # Arrange: ensure open would explode if called (we expect it not to be called)
    def _boom(*args, **kwargs):
        raise AssertionError("open() should not be called for absolute paths")

    monkeypatch.setattr("builtins.open", _boom)

    # Act
    result = ssrf_lab(os.path.abspath(str(tmp_path / "secret.txt")))

    # Assert
    assert result == {"blog": "No blog found"}


def test_ssrf_lab_rejects_directory_traversal(monkeypatch):
    """Regression: traversal must not escape base_dir."""
    def _boom(*args, **kwargs):
        raise AssertionError("open() should not be called for traversal attempts")

    monkeypatch.setattr("builtins.open", _boom)

    result = ssrf_lab("../secret.txt")
    assert result == {"blog": "No blog found"}
