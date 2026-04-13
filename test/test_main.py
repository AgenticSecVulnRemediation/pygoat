import builtins

import pytest

from introduction.playground.ssrf import main


def test_ssrf_lab_rejects_traversal_and_does_not_open(monkeypatch):
    # Arrange
    opened = {"called": False}

    def fake_open(*args, **kwargs):
        opened["called"] = True
        raise AssertionError("open() should not be called")

    monkeypatch.setattr(builtins, "open", fake_open)

    # Act
    result = main.ssrf_lab("../etc/passwd")

    # Assert
    assert result == {"blog": "Invalid file path."}
    assert opened["called"] is False


def test_ssrf_lab_rejects_absolute_path_and_does_not_open(monkeypatch):
    # Arrange
    opened = {"called": False}

    def fake_open(*args, **kwargs):
        opened["called"] = True
        raise AssertionError("open() should not be called")

    monkeypatch.setattr(builtins, "open", fake_open)

    # Act
    result = main.ssrf_lab("/etc/passwd")

    # Assert
    assert result == {"blog": "Invalid file path."}
    assert opened["called"] is False
