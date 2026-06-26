import builtins
import os

import pytest

# Assumption: introduction.playground.ssrf.main is importable in tests.
from introduction.playground.ssrf.main import ssrf_lab


def test_ssrf_lab_rejects_path_traversal_outside_base_dir(monkeypatch):
    # Arrange: make __file__ resolve to a stable base directory
    base_dir = "/app/introduction/playground/ssrf"
    monkeypatch.setattr(
        "introduction.playground.ssrf.main.__file__",
        os.path.join(base_dir, "main.py"),
        raising=False,
    )

    opened = {"called": False}

    def fake_open(*args, **kwargs):
        opened["called"] = True
        raise AssertionError("open() must not be called for traversal")

    monkeypatch.setattr(builtins, "open", fake_open)

    # Act
    result = ssrf_lab("../secrets.txt")

    # Assert
    assert result == {"blog": "No blog found"}
    assert opened["called"] is False
