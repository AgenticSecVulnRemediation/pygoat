import os
import pathlib


def test_ssrf_lab_blocks_absolute_paths(tmp_path, monkeypatch):
    # Arrange
    from introduction.playground.ssrf.main import ssrf_lab

    # Act
    result = ssrf_lab(str(tmp_path / 'secret.txt'))

    # Assert
    assert result == {"blog": "No blog found"}


def test_ssrf_lab_blocks_dotdot_paths(tmp_path, monkeypatch):
    # Arrange
    from introduction.playground.ssrf.main import ssrf_lab

    # Act
    result = ssrf_lab("../secrets.txt")

    # Assert
    assert result == {"blog": "No blog found"}
