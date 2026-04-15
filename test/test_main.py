import os

import pytest

from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_absolute_path_to_prevent_traversal(monkeypatch):
    # Arrange
    opened = {"called": False}

    def fake_open(*args, **kwargs):
        opened["called"] = True
        raise AssertionError("open() must not be called for rejected paths")

    monkeypatch.setattr("builtins.open", fake_open)

    # Act
    result = ssrf_lab("/etc/passwd")

    # Assert
    assert result == {"blog": "No blog found"}
    assert opened["called"] is False


def test_ssrf_lab_rejects_parent_directory_traversal(monkeypatch):
    # Arrange
    opened = {"called": False}

    def fake_open(*args, **kwargs):
        opened["called"] = True
        raise AssertionError("open() must not be called for rejected paths")

    monkeypatch.setattr("builtins.open", fake_open)

    # Act
    result = ssrf_lab("../secrets.txt")

    # Assert
    assert result == {"blog": "No blog found"}
    assert opened["called"] is False
